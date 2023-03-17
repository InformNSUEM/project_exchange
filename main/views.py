from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from users.forms import AuthCustomForm
from users.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
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
                    self.data.update({"success": False, "error": "Пользователь не подтвержден"})
                    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        return JsonResponse(self.data)
                else:
                    print(user)
                    login(request, user)
                    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        print(self.data)
                        return JsonResponse(self.data)
        else:
            self.data.update({"success": False, "error": "Email или пароль не верный"})
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse(self.data)
            


        return super().post(request, *args, **kwargs)



class MyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        
        print(request)
        data = JSONParser().parse(request)
        print(data)
        # здесь обрабатываем POST запрос
        return Response({'message': 'Success!'}, status=status.HTTP_200_OK)
    


class GalaryNsuemView(TemplateView):

    template_name = "main/nsuem_gal.html"

class BaseOrderView(TemplateView):

    template_name = "main/base_gal.html"

class AuthorityOrderView(TemplateView):

    template_name = "main/orders_gal.html"
