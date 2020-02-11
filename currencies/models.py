from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=200)
    change = models.CharField(max_length=10, blank=True, default="0%")
    value = models.FloatField(validators=[MinValueValidator(0)])
    slug = models.SlugField(unique=True, primary_key=True)
    image = models.URLField()

    @staticmethod
    def currency_converter(currency1, currency2):
        return currency1.value/currency2.value

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        if Currency.objects.filter(pk=self.pk).exists():
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send(
                'currencies_notifications', 
                {
                    'type': 'currency_update', 
                    'instance': self,
                },

                )
            )
        return super().save(**kwargs)

    def __str__(self):
        return self.name