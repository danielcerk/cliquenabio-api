from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('password-reset/confirm/<uidb64>/<token>/',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    path('password-reset/',
        TemplateView.as_view(template_name="password_reset.html"),
        name='password-reset'),
    path('password-reset/confirm/',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password-reset-confirm'),
    path('password-change/',
        TemplateView.as_view(template_name="password_change.html"),
        name='password-change'),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
]
