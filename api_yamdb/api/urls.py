from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import get_code, get_token, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', get_code),
    path('v1/auth/token/', get_token),
    path('v1/', include(router.urls)),
]
