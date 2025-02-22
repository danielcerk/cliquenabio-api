from django.urls import path
from .views import ProfileDetailView, AuthenticatedUserProfileView

urlpatterns = [
    
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
    path('account/me/profile/', AuthenticatedUserProfileView.as_view(), name='authenticated-user-profile'),

]
