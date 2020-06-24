import json
import unittest
from datetime import datetime
from http import HTTPStatus

import pytest
from django.test import RequestFactory
from server.endpoints.currency_exchange import get_currency_exchanges_endpoint
from server.models.currency_exchange import CurrencyExchange


class TestCurrencyExchangesEndpoint(unittest.TestCase):
    @pytest.mark.django_db
    def test_it_returns_empty_currency_exchanges(self):
        request = RequestFactory().get('/currency-exchanges')
        response = get_currency_exchanges_endpoint(request)

        assert response.status_code == HTTPStatus.OK
        assert response.content == b'[]'

    @pytest.mark.django_db
    def test_it_returns_currency_exchanges_list_with_one_element(self):
        CurrencyExchange.objects.create(
            symbol='BTC-USDT',
            high=200.23,
            low=10.23,
            updated_at=datetime(2019, 1, 1)
        )

        request = RequestFactory().get('/currency-exchanges')
        response = get_currency_exchanges_endpoint(request)

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == [{
            'symbol': 'BTC-USDT',
            'high': 200.23,
            'low': 10.23,
            'updated_at': '2019-01-01T00:00:00Z'
        }]

    @pytest.mark.django_db
    def test_it_returns_currency_exchanges_list_with_many_elements(self):
        CurrencyExchange.objects.create(
            symbol='BTC-USDT',
            high=200.23,
            low=10.23,
            updated_at=datetime(2019, 1, 1)
        )
        CurrencyExchange.objects.create(
            symbol='BTC-USDT',
            high=220.23,
            low=10.23,
            updated_at=datetime(2019, 1, 2)
        )

        request = RequestFactory().get('/currency-exchanges')
        response = get_currency_exchanges_endpoint(request)

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == [
            {
                'symbol': 'BTC-USDT',
                'high': 200.23,
                'low': 10.23,
                'updated_at': '2019-01-01T00:00:00Z'
            },
            {
                'symbol': 'BTC-USDT',
                'high': 220.23,
                'low': 10.23,
                'updated_at': '2019-01-02T00:00:00Z'
            },
        ]
