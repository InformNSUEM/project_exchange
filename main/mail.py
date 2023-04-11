from django.core.mail import send_mail
from django.template.loader import render_to_string
from users.user_models import User



def send_request_approve(customer_request):
   

    message = render_to_string('main/mail/request_mail.html', {
    'user': customer_request["customer"],
    'request_id': customer_request["id"],
    })
    email_subject = "Заявка на выполнение работы"

    send_mail(email_subject, message, "birzha@nsuem.ru", [customer_request["email"]], fail_silently=False)