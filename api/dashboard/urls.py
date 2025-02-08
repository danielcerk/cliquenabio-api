from django.urls import path

from .views import DashboardView, AdminDashboardView

urlpatterns = [
    path('account/dashboard/', DashboardView.as_view(), name='dashboard-user'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='dashboard-admin'),
]
