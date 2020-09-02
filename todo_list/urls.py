from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'todo_list'

urlpatterns = [
    path('todolist/', views.todolist, name = 'todolist'),
    path('todohistory/', views.todohistory, name = 'todohistory'),
    path('todoremove/<int:pk>', views.todoremove, name="todoremove"),
    path('todorecovery/<int:pk>', views.todorecovery, name="todorecovery"),
    path('todocmplt/<int:pk>', views.todocmplt, name="todocmplt"),
]