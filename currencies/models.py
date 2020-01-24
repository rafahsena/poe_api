from django.db import models
from django.utils.text import slugify

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=200)
    change = models.CharField(max_length=10, blank=True, default="0%")
    value = models.FloatField()
    slug = models.SlugField(unique=True, primary_key=True)

    @staticmethod
    def currency_converter(currency1, currency2):
        return currency1/currency2

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name