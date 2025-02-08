from django.urls import path

from .views import ContactEmailAPIView, FormContactEmailAPIView

urlpatterns = [
    
    path('account/<int:id>/send-email/', ContactEmailAPIView.as_view(), name='send-email'),
    path('account/form-email/', FormContactEmailAPIView.as_view(), name='form-email'),

]
