from django.urls import path

from rest_framework.authtoken import views
from .views import MeView, RegisterUserView, EmailConfirmationView, \
    PasswordRecoveryView, PasswordRecoveryConfirmationView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/v1/users/token/', views.obtain_auth_token),
    path('api/v1/users/me', MeView.as_view()),
    path('api/v1/users/register', RegisterUserView.as_view(), name='api-v1-user-register'),
    path('api/v1/users/confirm-email', EmailConfirmationView.as_view(), name='api-v1-user-confirm-email'),
    path('api/v1/users/request-password-recovery', PasswordRecoveryView.as_view(), name='api-v1-user-request-password-recovery'),
    path('api/v1/users/confirm-password-recovery', PasswordRecoveryConfirmationView.as_view(),
         name='api-v1-user-confirm-password-recovery'),
]