from http import HTTPStatus

import requests


BTC_USDT_SYMBOL = 'BTC-USDT'
BITTREX_CURRENCY_EXCHANGE_SUMMARY_API_ENDPOINT = 'https://api.bittrex.com/v3/markets/{symbol}/summary'


def summary(symbol):
    response = requests.get(BITTREX_CURRENCY_EXCHANGE_SUMMARY_API_ENDPOINT.format(symbol=symbol))

    if response.status_code != HTTPStatus.OK:
        raise GetCurrencyExchangeSummaryError(
            f'Unable to retrieve {symbol} currency exchange. Error {response.status_code}'
        )

    return response.json()


class GetCurrencyExchangeSummaryError(RuntimeError):
    pass
