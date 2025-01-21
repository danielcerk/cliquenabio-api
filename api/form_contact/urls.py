from django.urls import path

from .views import FormContactAPIView

urlpatterns = [
    
    path('send-email/', FormContactAPIView.as_view(), name='send-email')

]
