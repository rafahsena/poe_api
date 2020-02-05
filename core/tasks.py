from core.get_html import update_currencies
from celery import shared_task
import time
from celery import task

@task
def update_all_currencies():
    update_currencies('https://poe.ninja/challenge/currency')
    return True