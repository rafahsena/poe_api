from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from currencies.api.serializers import CurrencySerializer, CurrencyListSerializer
from currencies.models import Currency
from rest_framework.decorators import action
from rest_framework.response import Response

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (BearerAuthentication, )

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is 
            print("oi")
            if isinstance(data, list):
                kwargs["many"] = True
                print('alooooooo')

        return super().get_serializer(*args, **kwargs)

    @action(methods=['put'], detail=False)
    def bulk_update(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(data=request.data, instance=qs, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)