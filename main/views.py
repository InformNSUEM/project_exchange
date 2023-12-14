from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from users.forms import AuthCustomForm, UserCreationFormCustom
from users.models import User, UserProfile
from main.models import CustomerGoal, DepthTask, Program, ApplicationBuisness
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from users.tasks import send_authorize_email
from .forms import ApplicationAuthorityForm
from django.views.generic.edit import CreateView

from .validators import BuisnessAppValidator, UserValidator

from .tasks import send_request_mail, send_buisness_request_mail
from .mail import send_buisness_request_approve

from django.conf import settings
from django.contrib.auth.decorators import login_required

class MainView(TemplateView):

    template_name = "main/index.html"
    form_class = AuthCustomForm
  
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }
        print(settings.SITE_NAME)

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

class Business_App(View):

    template_name = 'main/business.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

        self.postData = {}
    
    def get(self, request, *args, **kwargs):
     
        
        goals = CustomerGoal.objects.all().order_by("id")
        depths = DepthTask.objects.all().order_by("name")
        programs = Program.objects.select_related("eduLevel").all().order_by("name")
        context = {}

        context['goals'] = goals
        context['depths'] = depths
        context['programs'] = programs
      

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

            self.postData = request.POST.dict()
            
            self.postData.update({"purpose":request.POST.getlist("purpose")})
            self.postData.update({"depthTask":request.POST.getlist("depthTask")})
            self.postData.update({"program":request.POST.getlist("program")})

          
            is_valid, errors = BuisnessAppValidator(self.postData, ApplicationBuisness).validate()

            if is_valid:
               
                form_data_instance = ApplicationBuisness(
                    customer = self.postData.get("customer"),
                    department = self.postData.get("department"),
                    fio = self.postData.get("fio"),
                    post = self.postData.get("post"),
                    phone_number = self.postData.get("phone_number"),
                    email = self.postData.get("email"),
                    task_formulation = self.postData.get("task_formulation"),
                    problem_formulation = self.postData.get("problem_formulation"),
                    relevance = self.postData.get("relevance"),
                    completion_dates  = self.postData.get("completion_dates"),
                    research_purpose = self.postData.get("research_purpose"),
                    key_words = self.postData.get("key_words"),
                    wish_result = self.postData.get("wish_result"),
                    other_info = self.postData.get("other_info")
                )

                form_data_instance.save()

                form_data_instance.purpose.add(*self.postData.get("purpose"))
                form_data_instance.depthTask.add(*self.postData.get("depthTask"))
                form_data_instance.program.add(*self.postData.get("program")) 
                self.data.update({"id":form_data_instance.id})
                self.postData.update({"id":form_data_instance.id})
                

                send_buisness_request_mail.delay(self.postData) 

                return JsonResponse(self.data)


        
            
    
    
        
      
          
  

class GalaryNsuemView(TemplateView):

    template_name = "main/nsuem_gal.html"

class BaseOrderView(TemplateView):

    template_name = "main/base_gal.html"

class AuthorityOrderView(TemplateView):

    template_name = "main/orders_gal.html"



def register(request):


        

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        

        postData = request.POST.dict()
 
        form = UserCreationFormCustom(postData)
     
        if form.is_valid():

            print("Nice")

            user = form.save(commit=False)
            user.is_active = False
            user.email = form.cleaned_data.get('email')
            user.save()

            profile = UserProfile.objects.create(user=user)

            profile.university_name = form.cleaned_data.get('university_name')
            profile.post = form.cleaned_data.get('post')
            profile.department = form.cleaned_data.get('department')
            profile.cathedra = form.cleaned_data.get('cathedra')
            profile.phone = form.cleaned_data.get('phone')
            profile.save()
            user_dict = model_to_dict(user)
       
            send_authorize_email.delay(user = user_dict)

            print("Nice")

            return JsonResponse({"success": True, "errors": None, "email":user.email})
        else:
            print(form.errors.as_data())
            return JsonResponse({"success": False, "errors": form.errors})



   

      
@login_required(login_url = 'login')
def user_logout(request):
   logout(request)
   return redirect("/")