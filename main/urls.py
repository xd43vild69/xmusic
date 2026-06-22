from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('button-action/', views.button_action, name='button_action'),
]