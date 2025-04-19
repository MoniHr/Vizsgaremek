from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')

# Load Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'check_job_post_expirations': {
        'task': 'jobs.tasks.send_expiration_reminders',
        'schedule': crontab(hour=0, minute=0),  # Every night at midnight
    },
}

# Debugging task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
