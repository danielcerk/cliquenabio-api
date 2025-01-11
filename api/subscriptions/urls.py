from django.urls import path
from .views import (
    CancelSubscriptionAPIView, 
    CreateSubscriptionAPIView,
    AttachPaymentMethodAPIView,
    UpdatePlanAPIView,
    StripeWebhookAPIView,
)

urlpatterns = [
    path('create-subscription/', CreateSubscriptionAPIView.as_view(), name='create-subscription'),
    path('cancel-subscription/', CancelSubscriptionAPIView.as_view(), name='cancel-subscription'),
    path('attach-payment-method/', AttachPaymentMethodAPIView.as_view(), name='attach-payment-method'),
    path('update-plan/', UpdatePlanAPIView.as_view(), name='update-plan'),
    path('stripe/webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'),
]
