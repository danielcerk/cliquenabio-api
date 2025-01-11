import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (

    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS

)
from django.conf import settings
from rest_framework import status
from .utils import update_subscription_plan
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret_key = settings.STRIPE_ENDPOINT_SECRET

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.created_by == request.user

class CreateSubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def post(self, request, *args, **kwargs):

        user = request.user
        plan_id = request.data.get('plan_id')

        subscription = Subscription.objects.get(user=user)

        stripe_subscription = stripe.Subscription.create(
            customer=subscription.stripe_customer_id,
            items=[{"price": plan_id}],
        )

        price_id = stripe_subscription["items"]["data"][0]["price"]["id"]
        price = stripe.Price.retrieve(price_id)
        product_id = price["product"]
        product = stripe.Product.retrieve(product_id)

        subscription.stripe_subscription_id = stripe_subscription['id']

        if product.get('name') == 'Conexão':

            subscription.plan = subscription.Plan.CONEXAO

        elif product.get('name') == 'Influência':

            subscription.plan = subscription.Plan.INFLUENCIA

        else:

            raise ValueError(f"Nome do produto inesperado: {product.get('name')}")
        
        subscription.active = True

        subscription.save()

        return Response({"message": "Assinatura criada com sucesso", "subscription_id": stripe_subscription['id']})

class CancelSubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def post(self, request, *args, **kwargs):

        user = request.user

        subscription = Subscription.objects.get(user=user)

        stripe.Subscription.delete(subscription.stripe_subscription_id)

        subscription.plan = subscription.Plan.GRATIS
        subscription.active = True

        subscription.save()

        return Response({"message": "Assinatura cancelada com sucesso"})

class AttachPaymentMethodAPIView(APIView):

    def post(self, request):

        customer_id = request.data.get("customer_id")
        payment_method_id = request.data.get("payment_method_id")

        if not customer_id or not payment_method_id:

            return Response(
                {"error": "customer_id and payment_method_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)

            stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": payment_method_id},
            )

            return Response({"message": "Payment method attached successfully."})

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePlanAPIView(APIView):

    def post(self, request, *args, **kwargs):

        subscription_id = request.data.get("subscription_id")
        new_price_id = request.data.get("new_price_id")

        if not subscription_id or not new_price_id:

            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)

        updated_subscription = update_subscription_plan(subscription_id, new_price_id)

        if updated_subscription:

            return Response({"message": "Plano atualizado com sucesso", "subscription": updated_subscription})
        
        return Response({"error": "Erro ao atualizar plano"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StripeWebhookAPIView(APIView):

    def post(self, request, *args, **kwargs):

        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = webhook_secret_key

        try:

            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

        except ValueError:

            return Response({"error": "Invalid payload"}, status=400)
        
        except stripe.error.SignatureVerificationError:

            return Response({"error": "Invalid signature"}, status=400)

        if event['type'] == 'invoice.payment_succeeded':

            subscription_id = event['data']['object']['subscription']
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
            subscription.active = True
            subscription.save()

        elif event['type'] == 'invoice.payment_failed':
            
            pass

        return Response({"message": "Evento processado com sucesso"})
