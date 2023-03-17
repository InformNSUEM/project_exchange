
from django.urls import path, include
from .views import MainView, GalaryNsuemView, BaseOrderView, AuthorityOrderView, MyAPIView


urlpatterns = [
    path("", MainView.as_view(), name = "main"),
    path("accounts/", include("users.urls")),
    path("nsuem_gal", GalaryNsuemView.as_view(), name = "nsuem_galary"),
    path("base_gal", BaseOrderView.as_view(), name = "base_galary"),
    path("authority_gal", AuthorityOrderView.as_view(), name = "authority_galary"),
    path('my-api/', MyAPIView.as_view(), name='my-api'),
        
] 

