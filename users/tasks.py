

from exchange.celery import app
from .mail import send_email

@app.task
def send_authorize_email(user):
    send_email(user)