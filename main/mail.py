from datetime import datetime
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from users.user_models import User
from django.utils.html import strip_tags
from .models import CustomerGoal, DepthTask, Program



def send_request_approve(customer_request):
   

    message = render_to_string('main/mail/request_mail.html', {
    'user': customer_request["customer"],
    'request_id': customer_request["id"],
    })
    email_subject = "Заявка на выполнение работы"

    send_mail(email_subject, message, "birzha@nsuem.ru", [customer_request["email"]], fail_silently=False)

def send_buisness_request_approve(mail_data):
    
    purposes = CustomerGoal.objects.filter(pk__in =  mail_data["purpose"])
    mail_data.update({"purpose": ", ".join(str(f"{x.name}") for x in purposes ) }) 
    depthTask = DepthTask.objects.filter(pk__in = mail_data["depthTask"])
    mail_data.update({"depthTask": ", ".join(str(f"{x.name}") for x in depthTask ) }) 

    if mail_data.get("program"):
        program = Program.objects.filter(pk__in = mail_data["program"])
        mail_data.update({"program": ", ".join(str(f"{x.name}") for x in program ) }) 
    else:
         mail_data.update({"program": ""})

    date_string = mail_data["completion_dates"]


    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    mail_data.update({"completion_dates": date_object.strftime("%d.%m.%Y")})


    html_message = render_to_string('main/mail/buisness_app_mail.html', mail_data)

    plain_message = strip_tags(html_message)
    email_subject = "Заявка на выполнение работы"
   
    send_mail(email_subject, plain_message, "birzha@nsuem.ru", [mail_data["email"]], html_message=html_message)



