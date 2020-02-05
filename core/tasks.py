from core.get_html import update_currencies
from celery import task

@task
def update_all_currencies():
    update_currencies('https://poe.ninja/challenge/currency')
