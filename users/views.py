from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomerUserCreationForm, StudentUserCreationForm, AuthCustomForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group

from django.utils.encoding import force_str
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User, StudentUser, CustomerUser
from django.shortcuts import render


from .tandem import StudentData
from django.http import JsonResponse
from main import models as mainmodels
from .tasks import send_authorize_email
from django.forms.models import model_to_dict

class RegisterCustomerView(CreateView):

    form_class = CustomerUserCreationForm
    template_name = 'users/register.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["reg_name"] = "Регистрация заказчика"
        context["form_url"] = "registerCustomer"
        context["form_class"] = "register-form-customer"
        context["success_message"] = "Письмо с подтверждением аккаунта отправлено вам на почту"
        return context
    
    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.email = form.cleaned_data.get('email')
            user.save()
            user.groups.add(Group.objects.get(name = "Заказчик")) 

            profile = CustomerUser.objects.create(user=user)
            profile.customer = form.cleaned_data.get('customer')
            profile.post = form.cleaned_data.get('post')
            profile.save()
            user = model_to_dict(user)
            del user['groups']
            send_authorize_email.delay(user = user)

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse(self.data)
        else:        
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'errors': form.errors})
                return render(request, self.template_name, {'form': form})

    
class RegisterStudentView(CreateView):

    form_class = StudentUserCreationForm
    template_name = 'users/register.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация исполнителя'
        context["reg_name"] = "Регистрация исполнителя"
        context["success_message"] = "Письмо с подтверждением аккаунта отправлено вам на почту"
        context["form_url"] = "registerStudent"
        context["form_class"] = "register-form-student"
        return context


    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            user = form.save(commit=False)
        
            try:
                student = StudentData().get(form.cleaned_data.get('booknumber'))
            except:
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    self.data.update({"success": False, "error": "Сервер не доступен, попробуйте позже"})
                    return JsonResponse(self.data)
                
            if student:
                user.last_name = student.lastname
                user.first_name = student.firstname
                user.email = student.email
                user.patronymic = student.partonymic
                user.is_active = False
                user.save()
                user.groups.add(Group.objects.get(name = "Исполнитель")) 
            else:
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    self.data.update({"success": False, "error": "Студент с данным номером зачетки не найден"})
                    return JsonResponse(self.data)
            
            profile = StudentUser.objects.create(user=user)
            profile.booknumber = form.cleaned_data.get('booknumber')
            profile.dateBith = student.datebirth
            profile.group = mainmodels.Group.objects.get(name = student.group)
            profile.save()
           
            user = model_to_dict(user)
            del user['groups']
           
            send_authorize_email.delay(user = user)


            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse(self.data)
            
        else:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            return render(request, self.template_name, {'form': form})
        

class CustomLoginView(LoginView):

    template_name = "users/login.html"
    form_class = AuthCustomForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["reg_name"] = "Вход в систему"
        return context
   


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

    return render(request, 'users/email_confimed.html')
