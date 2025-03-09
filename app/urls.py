from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView

urlpatterns = [
    path('api/v1/auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('api/v1/auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('api/v1/auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
]

if settings.DEBUG:

    urlpatterns.append(path("admin/", admin.site.urls))