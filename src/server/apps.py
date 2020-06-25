import logging
from datetime import datetime

from currency_exchange import currency_exchange_service
from currency_exchange.currency_exchange_service import BTC_USDT_SYMBOL, GetCurrencyExchangeSummaryError
from dateutil.parser import isoparse
from django.apps import AppConfig
import periodic_task


BTC_USDT_UPDATE_INTERVAL = 10


class Server(AppConfig):
    name = 'server'
    verbose_name = "Market Graph"

    def ready(self):
        self.task = periodic_task.PeriodicTask(BTC_USDT_UPDATE_INTERVAL, _store_btc_usdt_currency_exchange)
        self.task.start()


def _store_btc_usdt_currency_exchange():
    from server.models.currency_exchange import CurrencyExchange

    try:
        btc_usdt_summary = currency_exchange_service.summary(BTC_USDT_SYMBOL)
    except GetCurrencyExchangeSummaryError as error:
        logging.warning(str(error))
        return

    CurrencyExchange.objects.create(
        symbol=btc_usdt_summary['symbol'],
        high=float(btc_usdt_summary['high']),
        low=float(btc_usdt_summary['low']),
        updated_at=isoparse(btc_usdt_summary['updatedAt']),
    )
