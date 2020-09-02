from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/',views.profile, name='profile'),
    path('org/',views.orgChart, name='org'),
    path('target/',views.targetPopup, name='target'),
    path('modified/',views.modifiedProfile, name='modified'),
    path('changepw/',views.changepw, name='changepw'),
    path('join/',views.register, name='join'),
    path('notify/',views.notify, name='notify'),
    path('thanks/', TemplateView.as_view(template_name='accounts/thanks.html'), name='thanks'),
    path('management/',views.management, name='management'),
    path('manage_detail/<int:pk>',views.manage_detail, name='manage_detail'),
    path('annualapproval/',views.annual_approval_line, name='annualapproval'),
    path('annualapproval/<int:pk>/',views.annual_approval_line_detail, name='annualapproval_detail'),
]
