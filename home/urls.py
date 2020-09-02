from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
   
    path('filemenual/', TemplateView.as_view(template_name='filemenual.html'),name='filemenual'),
    path('newManual/', TemplateView.as_view(template_name='newManual.html'),name='newManual'),
    path('existManual/', TemplateView.as_view(template_name='existManual.html'),name='existManual'),
    path('faq/', TemplateView.as_view(template_name='faq.html'),name='faq'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('target/', views.signout, name='logout'),
    path('main/', views.main, name='main'),
    path('', views.main, name='main'),
    path('git/', views.git, name='git'),
    path('status/', views.status, name='status'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt",
         content_type='text/plain')),

    
]