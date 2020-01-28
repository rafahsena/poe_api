from rest_framework.test import APITestCase
from django.urls import reverse
from currencies.models import Currency
from rest_framework import status
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your tests here.

class CurrencySerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('teste', 'a@a.com', 'teste')

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
        user = User.objects.get(username='teste')
        self.client.force_authenticate(user)

        mock = {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}
        url = reverse('currency-list')
        response = self.client.post(url, mock, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        obj = Currency.objects.get(slug='chaos-orb')
        self.assertEqual(obj.value, 150)

        self.client.force_authenticate(user=None)

    def test_authenticated_currency_bulk_update(self):
        user = User.objects.get(username='teste')
        self.client.force_authenticate(user)

        currency = {'name' : 'Chaos Orb', 'value': 150, 'change' : '+7%', 'slug': 'chaos-orb'}
        Currency.objects.create(**currency)

        mock = [
                {'name' : 'Chaos Orb', 'value': 1, 'change' : '-70%', 'slug': 'chaos-orb'}, 
                {'name' : 'Exalted Orb', 'value': 1, 'change' : '-70%', 'slug': 'exalted-orb'}, 
               ]
        url = reverse('currency-bulk-update')
        response = self.client.put(url, mock, format='json')
        obj = Currency.objects.get(pk='chaos-orb')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.value, 1)

        self.client.force_authenticate(user=None)