from django.urls import path
from login import views

urlpatterns = [
    path('login_handler', views.login),
]