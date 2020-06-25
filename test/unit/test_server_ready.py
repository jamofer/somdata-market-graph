import unittest
from datetime import datetime

from dateutil.tz import UTC
from mock import patch, MagicMock

from currency_exchange.currency_exchange_service import BTC_USDT_SYMBOL, GetCurrencyExchangeSummaryError
from server import apps
from server.apps import BTC_USDT_UPDATE_INTERVAL, Server


class TestServerReady(unittest.TestCase):
    def setUp(self) -> None:
        self.task = MagicMock()
        self.PeriodicTask = patch('periodic_task.PeriodicTask').start()
        self.CurrencyExchange = patch('server.models.currency_exchange.CurrencyExchange').start()
        self.currency_exchange_summary = patch('currency_exchange.currency_exchange_service.summary').start()
        self.PeriodicTask.return_value = self.task

        class ServerStub(Server):
            def __init__(self):
                pass
        self.server = ServerStub()

    def tearDown(self) -> None:
        patch.stopall()

    def test_it_starts_currency_exchange_updater_with_one_minute_update_frequency_for_btc_usdt(self):
        self.server.ready()

        self.PeriodicTask.assert_called_once_with(BTC_USDT_UPDATE_INTERVAL, apps._store_btc_usdt_currency_exchange)
        self.task.start.assert_called_once()

    def test_it_stores_current_btc_usdt_currency_exchange_in_currency_exchange_server_model(self):
        self.currency_exchange_summary.return_value = {
            'symbol': 'BTC-USDT',
            'high': '9669.89899999',
            'low': '9210.99999998',
            'volume': '359.84717737',
            'quoteVolume': '3392124.43113383',
            'percentChange': '-4.0',
            'updatedAt': '2020-06-24T21:34:00.127Z'
        }

        apps._store_btc_usdt_currency_exchange()

        self.currency_exchange_summary.assert_called_once_with(BTC_USDT_SYMBOL)
        self.CurrencyExchange.objects.create.assert_called_once_with(
            symbol=BTC_USDT_SYMBOL,
            high=9669.89899999,
            low=9210.99999998,
            updated_at=datetime(2020, 6, 24, 21, 34, 0, 127000, tzinfo=UTC)
        )

    def test_it_ignores_error_retrieving_btc_usdt_currency_exchange(self):
        self.currency_exchange_summary.side_effect = GetCurrencyExchangeSummaryError

        apps._store_btc_usdt_currency_exchange()

        self.currency_exchange_summary.assert_called_once_with(BTC_USDT_SYMBOL)
        self.CurrencyExchange.objects.create.assert_not_called()
