from django.shortcuts import render
from django.http import HttpResponse
from users.models import CustomerUser
from django.views.generic.base import TemplateView
from main.forms import ApplicationAuthorityForm
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from main.models import ApplicationAuthority

from .tasks import send_request_mail

# Create your views here.

class MainView(TemplateView):

    template_name = "system/main.html"



class ProfileView(CreateView):

    template_name = "system/lk.html"
    form_class = ApplicationAuthorityForm


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }
    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)

        profile = CustomerUser.objects.get(user = self.request.user)
        context['profile'] = profile
        context['title'] = "Личная информация"
        return context


        
    
    def get(self, request, *args, **kwargs):

        

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            
            if "pk" in kwargs:

                _request = ApplicationAuthority.objects.get(pk = kwargs["pk"])
                html_response = render(request, 'system/lk_request_detail.html', {"title": "Информация по заявке", "request": _request})
            
                return HttpResponse(html_response.content)
            
            if kwargs["tab_id"] == "personal":
                
                profile = CustomerUser.objects.get(user = request.user)
                html_response = render(request, 'system/lk_profile.html', {"title": "Личная информация", "profile": profile})
            
                return HttpResponse(html_response.content)
            elif kwargs["tab_id"] == "my_requests":

                requests = ApplicationAuthority.objects.filter(customer = request.user).order_by("-created_at")
                
                html_response = render(request, 'system/lk_table.html', {"title": "Мои заявки", "requests":requests}, )
            
                return HttpResponse(html_response.content)
            else:

                form = ApplicationAuthorityForm
                html_response = render(request, 'system/lk_form.html', {"title": "Отправка заявки", "form":form})
            
                return HttpResponse(html_response.content)
  
        return super().get(request, *args, **kwargs)
    

    def post(self, request, *args: str, **kwargs):


        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if form.is_valid():

            print("Valid")

            customer_request = form.save(commit=False)
            customer_request.customer = request.user
            customer_request.save()
            
            customer_request.purpose.set(form.cleaned_data['purpose']) 
            customer_request.depthTask.set(form.cleaned_data['depthTask'])
            customer_request.key_words.set(form.cleaned_data['key_words'])
            customer_request.program.set(form.cleaned_data['program']) 

            
            customer_request = {
                "id": customer_request.id,
                "customer": customer_request.customer.get_respect_ask(),
                "email": customer_request.customer.email
                
            }
            
            send_request_mail.delay(customer_request = customer_request)

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse(self.data)
        else:
            print(form.errors)
            self.data.update({"success": False, "errors": form.errors})       
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse(self.data)
            
            return render(request, self.template_name, {'form': form})

    
        