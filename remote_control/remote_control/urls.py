"""remote_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from . import views, settings

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.home),
    re_path(r'^run/$', views.run),
    re_path(r'^cali/$', views.cali),
    re_path(r'^connection_test/$', views.connection_test),
]
