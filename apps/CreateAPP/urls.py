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
from django.urls import path,re_path
from apps.CreateAPP.views import DisplayCreateView,ModelUploadView,DeleteClearDataView,DownloadIconView,ReporteExcelView,\
    UploadIconView
app_name = 'CreateAPP'
urlpatterns = [
    re_path(r'^show/', DisplayCreateView.as_view(), name='show'),
    re_path(r'^upload/', ModelUploadView.as_view(), name='upload'),
    re_path(r'^clear/', DeleteClearDataView.as_view(), name='clear'),
    re_path(r'^dwicon/', DownloadIconView.as_view(), name='dwicon'),
    re_path(r'^iexcel/', ReporteExcelView.as_view(), name='iexcel'),
    re_path(r'^uploadapp/', UploadIconView.as_view(), name='uploadapp'),


]
