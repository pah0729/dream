from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = 'commute'

urlpatterns = [
    path('list/',views.commute_list, name='list'),
    path('detail/<int:pk>/',views.detail, name='detail'),
    path('detail_ajax/',views.detail_ajax, name='detail_ajax'),
    path('absenteeism/',views.absenteeism, name='absenteeism'),
]