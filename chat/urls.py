from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.ChatView, name='chat'),
    path('<str:room_name>/', views.SpecificChatView, name='specific_chat'),

]