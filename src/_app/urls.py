"""_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

from .settings import ENVIRONMENT

urlpatterns = [
    path('admin/', admin.site.urls),
]


# Swagger uses only in dev environment, but you can plug it for other envs too
if ENVIRONMENT == 'dev':
    from .env.openapi_urls import urlpatterns as openapi_urlpatterns
    urlpatterns += openapi_urlpatterns
