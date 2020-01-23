from django.db import models

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=200)
    change = models.CharField(max_length=10)
    value = models.FloatField()

    @staticmethod
    def currency_converter(currency1, currency2):
        return currency1/currency2