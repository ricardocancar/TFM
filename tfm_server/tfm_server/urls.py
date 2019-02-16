"""tfm_server URL Configuration

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

from clasifications.views import clasifications_detail_view, clasifications_create_view
from pre_classifications_content.views import  PreClassificationsContent_create_view, PreClassificationsContent_detail_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clasifications/', clasifications_detail_view),
    path('preclasificaitons/', PreClassificationsContent_detail_view),
]