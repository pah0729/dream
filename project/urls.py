from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'project'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('list/', views.list3, name='list'),
    path('todo/<int:pk>/',views.todo, name='todo_list'),
    path('detail/<int:pk>/',views.detail, name='todo_detail'),
    path('edit/<int:pk>/',views.edit, name='edit'),
    path('calendar/',views.CalendarView.as_view(template_name = 'project/project_calendar.html'), name='calendar'),
    path('stop/<int:pk>/',views.stop, name='stop'),
    path('indvd/', views.indvd, name='indvd'),
    path('history/', views.history, name='history'),
    
]