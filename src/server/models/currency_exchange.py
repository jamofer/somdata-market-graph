from django.db import models
from rest_framework import serializers


class CurrencyExchange(models.Model):
    symbol = models.TextField()
    high = models.FloatField()
    low = models.FloatField()
    updated_at = models.DateTimeField()


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = ('symbol', 'high', 'low', 'updated_at')
