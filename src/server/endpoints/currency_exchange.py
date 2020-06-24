from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.decorators import api_view
from server.models.currency_exchange import CurrencyExchange, CurrencyExchangeSerializer


@api_view(['GET'])
def get_currency_exchanges_endpoint(request):
    currency_exchanges = CurrencyExchange.objects.all()
    serialized_currency_exchanges = CurrencyExchangeSerializer(currency_exchanges, many=True)

    return JsonResponse(serialized_currency_exchanges.data, status=HTTPStatus.OK, safe=False)
