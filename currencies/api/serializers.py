from rest_framework import serializers
from currencies.models import Currency

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'slug', 'name', 'value', 'change')
        read_only_fields = ('id', 'slug')