from django.urls import path, include
from .views import AppVersionView


urlpatterns = [
    path('info/', AppVersionView.as_view(), name='info')
]