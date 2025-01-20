from django.urls import path
from .views import (
    CancelSubscriptionAPIView, 
    CreateSubscriptionAPIView,
    AttachPaymentMethodAPIView,
    UpdatePlanAPIView,
    StripeWebhookAPIView,
    GetPlansAPIView,
    PlanUserAPIView
)

urlpatterns = [
    path('plans/', GetPlansAPIView.as_view(), name='get-plans-stripe'), # Planos


    ########################## COLOCAR ID DO USUARIO NA ROTA ##########################

    path('plan/', PlanUserAPIView.as_view(), name='plan-user-stripe'), # Plano do usuário
    path('create-subscription/', CreateSubscriptionAPIView.as_view(), name='create-subscription'), # Fazer assinatura
    path('cancel-subscription/', CancelSubscriptionAPIView.as_view(), name='cancel-subscription'), # Cancelar assinatura
    path('attach-payment-method/', AttachPaymentMethodAPIView.as_view(), name='attach-payment-method'), # Metodo de pagamento
    path('update-plan/', UpdatePlanAPIView.as_view(), name='update-plan'), # Atualizar assinatura

    ###################################################################################

    path('stripe/webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'), # Monitorar
]
