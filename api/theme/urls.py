from rest_framework.routers import DefaultRouter

from .views import ThemeGlobalViewSet, ThemeUserAPIView

from django.urls import path, include

router = DefaultRouter()

router.register('themes', ThemeGlobalViewSet, basename='themes')

urlpatterns = [
    
    path('account/theme/', ThemeUserAPIView.as_view(), name='theme-user'),
    path('', include(router.urls)),

]
