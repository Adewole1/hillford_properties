# hillford_admin.urls

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from dj_rest_auth.registration.views import VerifyEmailView


schema_view = get_schema_view(
    openapi.Info(
        title='Hillford Properties',
        default_version='v1',
        description="A web API for managing hillford properties and tenants",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path("api-auth/", include('rest_framework.urls')),
    path("", include('properties.urls')),
    # path('', include('dj_rest_auth.urls')),
    # path('registration/', include('dj_rest_auth.registration.urls')),
    # path('account-confirm-email', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('allauth/', include('allauth.urls')),
    path("", include('authemail.urls')),
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    # path("tenants/", include('tenants.urls')),

    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
