import json
import unittest
from http import HTTPStatus

from currency_exchange import currency_exchange_service
from currency_exchange.currency_exchange_service import GetCurrencyExchangeSummaryError
from mock import patch
from pytest import raises
from requests import Response


class TestCurrencyExchangeService(unittest.TestCase):
    def setUp(self) -> None:
        self.get = patch('requests.get').start()

    def tearDown(self) -> None:
        patch.stopall()

    def test_it_returns_currency_exchange_summary(self):
        response_json = {
            'symbol': 'BTC-OTHER',
            'high': '9669.89899999',
            'low': '9210.99999998',
            'volume': '359.84717737',
            'quoteVolume': '3392124.43113383',
            'percentChange': '-4.0',
            'updatedAt': '2020-06-24T21:34:00.127Z'
        }
        response = Response()
        response._content = str(json.dumps(response_json)).encode('utf8')
        response.status_code = HTTPStatus.OK
        self.get.return_value = response

        result = currency_exchange_service.summary('BTC-OTHER')

        self.get.assert_called_once_with('https://api.bittrex.com/v3/markets/BTC-OTHER/summary')
        assert result == response_json

    def test_it_fails_getting_currency_exchange_summary_when_response_status_code_is_not_ok(self):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        with raises(GetCurrencyExchangeSummaryError):
            currency_exchange_service.summary('asdgersh"')
