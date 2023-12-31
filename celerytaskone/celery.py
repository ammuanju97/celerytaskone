from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerytaskone.settings')

app=Celery('celerytaskone')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery beat settings

app.conf.beat_schedule = {
      'send-email-every-day-at-14': {
          'task': 'send_email_app.tasks.send_mail_func',
          'schedule': crontab(hour=14, minute=18, day_of_month= 19, month_of_year = 6),
        #   'args': (2,) 
      }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    