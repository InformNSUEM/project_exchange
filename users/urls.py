from django.urls import path, include
from .views import RegisterCustomerView, RegisterStudentView, CustomLoginView, activate


urlpatterns = [
    path('register-customer', RegisterCustomerView.as_view(), name='registerCustomer'),
    path('register-student', RegisterStudentView.as_view(), name='registerStudent'),
    path('login', CustomLoginView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='account_activate'),
   # path('', include(('main.urls', 'main'), namespace='main'))
]