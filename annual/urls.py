from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'annual'

urlpatterns = [
    path('apply_list/',views.annual_list, name='list'),
    path('apply_list/<int:pk>/',views.confirm, name='confirm'),
    path('apply_approval/',views.approval_list, name='approval'),
    path('apply_approval/<int:pk>/',views.approval_detail, name='detail'),
    path('apply/',views.new, name='new'),
    path('apply_manage/',views.manage, name='manage'),
    path('plus/<int:pk>/',views.datemanage, name='datemanage'),
    path('remove/',views.removedate, name='remove'),
    path('minus/<int:pk>/',views.minusmanage, name='minusmanage'),
    path('total/',views.total, name='total'),
    path('calendar/',views.CalendarView.as_view(template_name = 'annual/calendar.html'), name='calendar'),
    path('modify/',views.modify, name='modify'),
    path('modify_minus/',views.modify_minus, name='modify_minus'),
]
