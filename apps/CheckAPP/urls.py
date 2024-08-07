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
from apps.CheckAPP.views import BaseAppView,AppListView,NextCheckView,CheckStatusView,UploadExcelView,UploadControlExcelView,LoadingVersionView,\
     DownloadingView,DownloadExcelTem,ClearDataView,ModifyAppView,CurrentModifyView,AddControlView,DelControlDataView,\
RunTaskView,StopTaskView,RedirectView,OAuthCallbackView,TestOAuthCallbackView

app_name = 'CheckAPP'
urlpatterns = [
    re_path(r'^$', BaseAppView.as_view(), name='index'),
    re_path(r'^search/',AppListView.as_view(),name="search"),
    re_path(r'^check/', NextCheckView.as_view(), name='check'),
    re_path(r'^upload/', UploadExcelView.as_view(), name='upload'),
    re_path(r'^uploadcontrol/', UploadControlExcelView.as_view(), name='uploadcontrol'),
    re_path(r'^loading/', LoadingVersionView.as_view(), name='loading'),
    re_path(r'^status/', CheckStatusView.as_view(), name='status'),
    re_path(r'^downloading$', DownloadingView.as_view(), name='downloading'),
    re_path(r'^rexcel',DownloadExcelTem.as_view(),name='rexcel'),
    re_path(r'^clear/',ClearDataView.as_view(),name='clear'),
    re_path(r'^modifying/',ModifyAppView.as_view(),name='modifying'),
    path(r'modify/<str:pkgname>/',CurrentModifyView.as_view(),name='modify'),
    re_path(r'^addcont/<str:pkgname>/',AddControlView.as_view(),name='modify'),
    re_path(r'^control/', AddControlView.as_view(), name='control'),
    re_path(r'^delControl/',DelControlDataView.as_view(),name='Delcontrol'),
    # re_path(r'^runTask/',RunTaskView.as_view(),name='runTask'),
    # re_path(r'^stopTask/',StopTaskView.as_view(),name='stopTask')
    re_path(r'oauth/callback/', OAuthCallbackView.as_view(), name='oauth_callback'),
    re_path(r'redirect/', RedirectView.as_view(), name='oauth_redirect'),
    re_path(r'test/callback/', TestOAuthCallbackView.as_view(), name='test_oauth_callback'),

]
