from django.urls import path
from .views import ProfileDetailView

urlpatterns = [
    
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile')

]
