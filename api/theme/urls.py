from django.urls import path
from .views import UserThemeAPIView

urlpatterns = [
    path('account/theme/', UserThemeAPIView.as_view(), name='user-theme'),
]
