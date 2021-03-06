"""disasterrest URL Configuration

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
from django.contrib import admin
from django.urls import path
import api.views as views
from django.conf.urls import url
from api.views import AlertList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search', views.search_database),
    path('api/search/', views.search_database),
    path('api/add', views.add_to_database),
    path('api/add/', views.add_to_database),
    path('api/searchWeb', AlertList.as_view()),
    path('api/searchWeb/', AlertList.as_view()),
    path('home', views.get_home),
    path('home/', views.get_home),
    path('', views.get_home),
    path('/', views.get_home),
    path('tutorial', views.get_search),
    path('tutorial/', views.get_search),
    url(r'^([\s\S]*)$', views.web_resource),
]
