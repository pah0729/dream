from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'notice'

urlpatterns = [
    path('list2/',views.list2, name='list'),
    path('explore/tags/<str:tag>/',views.list2, name='notice_search'),
    path('new/',views.new, name='new'),
    path('detail/<int:pk>/',views.detail, name='detail'),
    path('remove/<int:pk>/',views.remove, name='remove'),
    path('remove_comment/<int:pk>/',views.remove_comment, name='remove_comment'),
   
    path('case_list/',views.case_list, name='case_list'),
    path('explore_case/tags/<str:tag>/',views.case_list, name='case_search'),
    path('case_new/',views.case_new, name='case_new'),
    path('case_edit/<int:pk>/',views.case_edit, name='case_edit'),
    path('case_detail/<int:pk>/',views.case_detail, name='case_detail'),
    path('case_remove/<int:pk>/',views.case_remove, name='case_remove'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)