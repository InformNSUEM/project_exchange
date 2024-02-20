import requests
from django.conf import settings

def send_to_webhook(postData:dict):

    response = requests.post(settings.AIR_WEBHOOK_URL, json=postData)
    print(response.json())
    