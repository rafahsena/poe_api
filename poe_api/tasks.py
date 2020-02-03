from core.get_html import update_currencies
from celery import shared_task
import time

print('jlhlhjls')

@shared_task
def update_all_currencies():
    print('t´a rodando parssa')
    #update_currencies('https://poe.ninja/challenge/currency')
    time.sleep(5)
    return True

update_all_currencies.delay()