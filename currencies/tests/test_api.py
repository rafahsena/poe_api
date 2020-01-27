from rest_framework.test import APITestCase
from django.urls import reverse
from currencies.models import Currency
from rest_framework import status
from django.utils.text import slugify

# Create your tests here.

class CurrencySerializerTest(APITestCase):

    def test_currency_converter(self):
        pass

    def test_primary_key_is_slug(self):
        currency = Currency.objects.create(**{'name' : 'Exalted Orb', 'value': 150, 'change' : '+7%'})
        self.assertEqual(currency.slug, slugify(currency.name))

    def test_not_authenticated_currency_create(self):
        mock = {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}
        url = reverse('currency-list')
        response = self.client.post(url, mock, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_currency_bulk_update(self):
        mock = [
                {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}, 
                {'name' : 'Exalted Orb', 'value': 150, 'change' : '+7%'}
               ]
        url = reverse('currency-bulk-update')
        response = self.client.put(url, mock, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_currency_create(self):
        TOKEN = "db3a2e83dc3c77789a3abaed56611c4b14612860"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TOKEN)

        mock = {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}
        url = reverse('currency-list')
        response = self.client.post(url, mock, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
    

    def test_authenticated_currency_bulk_update(self):
        TOKEN = "db3a2e83dc3c77789a3abaed56611c4b14612860"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TOKEN)

        mock = [
                {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}, 
                {'name' : 'Exalted Orb', 'value': 150, 'change' : '+7%'}
               ]
        url = reverse('currency-bulk-update')
        response = self.client.put(url, mock, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials()
