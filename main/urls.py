
from django.urls import path
from .views import MainView, GalaryView


urlpatterns = [
    path("", MainView.as_view(), name = "main"),
    path("gal", GalaryView.as_view(), name = "galary"),
        
] 