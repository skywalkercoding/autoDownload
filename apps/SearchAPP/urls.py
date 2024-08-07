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

app_name = 'SearchAPP'
urlpatterns = [

    # re_path(r'^showsea', SearchKey.as_view(), name='showsea'),
    # re_path(r'^connecting$' , ConnectAppiumView.as_view() , name="connecting"),
    # re_path(r'^delete$' , DelAppView.as_view() , name="delete"),
    # re_path(r'^dexcel' , DownloadExcelView.as_view(),name="dxcel"),
    # re_path(r'^testing$' , TestingInfoView.as_view(),name="testing"),
    # re_path(r'^uploadapp$' , UploadAppView.as_view(),name="uploadapp"),
]
