import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos_project.settings")

app = Celery("kudos_project")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_connection_retry_on_startup = True

# Autodiscover tasks in Django apps
app.autodiscover_tasks()
