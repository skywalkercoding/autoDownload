"""AutoUpgradeApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.static import serve
from django.urls import path,re_path,include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path('^', include('apps.CheckAPP.urls', namespace="CheckAPP")),
    re_path('^2th/', include('apps.DownloadAPP.urls', namespace="2th")),
    re_path('^3th/', include('apps.UploadAPP.urls', namespace="3th")),
    re_path('^1th/', include('apps.CreateAPP.urls', namespace="1th")),
    re_path('^4th/', include('apps.SearchAPP.urls', namespace="4th")),
]
