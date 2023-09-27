from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from users.forms import AuthCustomForm
from users.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import ApplicationAuthorityForm
from django.views.generic.edit import CreateView

from .tasks import send_request_mail



class MainView(TemplateView):

    template_name = "main/index.html"
    form_class = AuthCustomForm
  
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)      
        context["title"] = "Интеллектуальная биржа"

        return context
    
    def authenticate(self, request, username=None, password=None, **kwargs):

        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        else:
            return None
        
    def post(self, request, *args: str, **kwargs):

        

        username = request.POST.get("email")
        password = request.POST.get("password")
      
        user = self.authenticate(request, username=username, password=password)

        if user:
                if user.is_active == False:
                    self.data.update({"success": False, "error": "Пользователь не активирован!<br>Пожалуйста перейдите по ссылке, отправленной вам на почту при прохождении регистрации"})
                    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        return JsonResponse(self.data)
                else:
                    print(user)
                    login(request, user)
                    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        print(self.data)
                        return JsonResponse(self.data)
        else:
            self.data.update({"success": False, "error": "Указанный Email или пароль не верны<br>Пожалуйста проверьте ваши данные и попробуйте снова"})
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse(self.data)
            


        return super().post(request, *args, **kwargs)


class GalaryNsuemView(TemplateView):

    template_name = "main/nsuem_gal.html"

class BaseOrderView(TemplateView):

    template_name = "main/base_gal.html"

class AuthorityOrderView(TemplateView):

    template_name = "main/orders_gal.html"
