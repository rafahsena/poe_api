import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poe_api.settings') #1

app = Celery('poe_api') #2
app.config_from_object('django.conf:settings', namespace='CELERY') #3
app.conf.beat_schedule = {
    'update-currencies-every-5-minutes': {
        'task': 'core.tasks.update_all_currencies',
        'schedule': 300.0,
    },
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #4
