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
from content_classificated.views import ClasificationsContent_detail_view
from resumen_values.views import  resumen_detail_view
from political_clasification.views import political_clasification_detail_view

urlpatterns = [
    path('', clasifications_detail_view),
    path('admin/', admin.site.urls),
    path('results/', ClasificationsContent_detail_view),
    path('summary_view/', resumen_detail_view)
]
