

from django.urls import path, include
from .views import MainView, GalaryNsuemView, BaseOrderView, AuthorityOrderView, Business_App, register, user_logout


urlpatterns = [
    path("", MainView.as_view(), name = "main"),
    path("accounts/", include("users.urls")),
    #path("nsuem_gal", GalaryNsuemView.as_view(), name = "nsuem_galary"),
    path("authority_galary", BaseOrderView.as_view(), name = "authority_galary"),
    path("nsuem_galary", AuthorityOrderView.as_view(), name = "nsuem_galary"),
    path("business_application", Business_App.as_view(), name = "business_application"),
    path("register", register, name = "register"),
    path("system/", include("system.urls")),
    path("logout", user_logout, name = "logout"),
 
        
] 

