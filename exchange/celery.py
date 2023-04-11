
from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange.settings")

app = Celery("exchange")
app.config_from_object("django.conf:settings", namespace = "CELERY")
app.autodiscover_tasks()