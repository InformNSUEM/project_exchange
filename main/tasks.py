
from exchange.celery import app
from .mail import send_request_approve

@app.task
def send_request_mail(customer_request):
    send_request_approve(customer_request)