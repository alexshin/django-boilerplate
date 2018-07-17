from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.conf import settings


PLATFORM_API_VERSION = settings.PLATFORM_API_VERSION


class AppVersionView(APIView,):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response({
            'platform': {
                'api_ver': PLATFORM_API_VERSION,
            }
        })