from django.urls import path
from home import views as home_views
from django.views.generic import TemplateView


urlpatterns = [
    path('', home_views.IndexView, name='index'),

]