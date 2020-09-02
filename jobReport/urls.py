from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jobreport'

urlpatterns = [
    path('list/',views.jobreport_list, name='list'),
    path('new/',views.new, name='new'),
    # path('apply/<int:pk>',views.apply, name='apply'),
    path('detail/<int:pk>/',views.detail, name='detail'),
    path('edit/<int:pk>/',views.edit, name='edit'),
    # path('remove/<int:pk>/',views.remove, name='remove'),
   
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)