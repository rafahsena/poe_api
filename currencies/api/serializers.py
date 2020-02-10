from rest_framework import serializers
from currencies.models import Currency

class CurrencyListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        currency_mapping = {currency.slug: currency for currency in instance}
        data_mapping = {item['slug']: item for item in validated_data}
        
        ret = []
        for currency_slug, data in data_mapping.items():
            currency = currency_mapping.get(currency_slug, None)
            if currency:
                ret.append(self.child.update(currency, data))

        return ret

class CurrencySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    class Meta:
        list_serializer_class = CurrencyListSerializer
        model = Currency
        fields = ('slug', 'name', 'value', 'change', 'image')
        read_only_fields = ('id', 'slug')
