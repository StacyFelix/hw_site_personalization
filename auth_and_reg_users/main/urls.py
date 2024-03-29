"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

import auth.views

urlpatterns = [
    path('', auth.views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', auth.views.signup),
    # path('login/', auth.views.login),
    # path('logout/', auth.views.logout),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
