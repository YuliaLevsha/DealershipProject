import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

app = Celery('DjangoProject')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule  = {
    'generate_cars': {
        'task': 'tasks.generate_cars',
        'schedule': crontab(minute='*/1'),
    },
    'generate_main': {
        'task': 'tasks.generate_main_objects',
        'schedule': crontab(minute='*/15'),
    },
    'buy_from_dealer': {
        'task': 'tasks.dealership_buy_from_dealer',
        'schedule': crontab(minute='*/25'),
    },
    'buy_from_dealership': {
        'task': 'tasks.customer_buy_from_dealership',
        'schedule': crontab(hour='*/30'),
    },
}
