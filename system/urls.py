
from django.urls import path, include
from .views import MainView, ProfileView

app_name = "system" 

urlpatterns = [
    path("", MainView.as_view(), name = "system"),
    path("profile", ProfileView.as_view(), name = "profile"),
    path("profile/<str:tab_id>/", ProfileView.as_view(), name = "content"),
    path("profile/my_requests/<int:pk>/", ProfileView.as_view(), name = "request_detail")

        
] 

