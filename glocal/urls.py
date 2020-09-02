"""glocal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib.auth.decorators import login_required
from ckeditor_uploader import views as views_ckeditor
from django.views.decorators.cache import never_cache
 
handler404 = 'home.views.handler404' 
handler500 = 'home.views.handler500' 

admin.site.site_header = "DREAMWARE Admin Portal"
admin.site.site_title = "드림웨어"
admin.site.index_title = "드림웨어 관리 포털"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("annual/", include("annual.urls")),
    path("", include("home.urls")),
    path("notice/", include("notice.urls")),
    path("commute/", include("commute.urls")),
    path("todo_list/", include("todo_list.urls")),  
    path("project/", include("project.urls")), 
    path("jobreport/", include("jobReport.urls")),
    path("upload/", login_required(views_ckeditor.upload), name='ckeditor_upload'),
    path("browse/", never_cache(login_required(views_ckeditor.browse)), name='ckeditor_browse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

