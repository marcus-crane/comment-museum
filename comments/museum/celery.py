import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'museum.settings')

import django
django.setup()

from celery import Celery
from celery.schedules import crontab
from archival import tasks

app = Celery('museum')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-streams-every-hour': {
        'task': 'archival.tasks.fetch_streams',
        'schedule': crontab(hour='*/1')
    },
    'fetch-comments-every-5-minutes': {
        'task': 'archival.tasks.fetch_comments',
        'schedule': crontab(minute='*/5')
    },
}