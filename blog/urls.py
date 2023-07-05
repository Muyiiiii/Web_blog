"""YJWEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='index'),
                  path('about/', views.about, name='about'),
                  path('contact/', views.contact, name='contact'),
                  path('submit/', views.submit, name='submit'),
                  path('login/', views.login, name='login'),
                  path('logout/', views.logout, name='logout'),
                  path('register/', views.register, name='register'),
                  path('more_info/', views.more_info, name='more_info'),
                  path('dianzan/', views.dianzan, name='dianzan'),
                  path('detail/', views.detail, name='detail'),
                  path('add/comment/', views.add_comment, name='add_comment'),
                  path('my/post/', views.mypost, name='mypost'),
                  path('edit/<int:moment_id>/', views.edit, name='edit'),
                  path('cinema/', views.cinema, name='cinema'),
                  path('admin/', views.admin, name='admin'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
