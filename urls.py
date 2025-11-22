from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('input/', views.input, name='input'), 
    path('output/', views.output, name='output'), 
]
