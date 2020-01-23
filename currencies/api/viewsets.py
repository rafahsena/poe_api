from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from currencies.api.serializers import CurrencySerializer
from currencies.models import Currency

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (BearerAuthentication, )
    