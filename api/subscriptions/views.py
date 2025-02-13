from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth import get_user_model
import stripe
from .models import Subscription, Plans

from datetime import datetime

# Configurando a chave secreta do Stripe
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret_key = settings.STRIPE_ENDPOINT_SECRET

class StripeWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = webhook_secret_key

        try:

            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        except ValueError as e:

            return Response({"error": "Invalid payload"}, status=400)
        
        except stripe.error.SignatureVerificationError as e:

            return Response({"error": "Invalid signature"}, status=400)

        # Identificar o tipo de evento recebido
        event_type = event.get("type")
        data = event.get("data", {}).get("object", {})

        try:

            if event_type == "customer.subscription.created":

                self.handle_subscription_created(data)

            elif event_type == "customer.subscription.updated":

                self.handle_subscription_updated(data)

            elif event_type == "customer.subscription.deleted":

                self.handle_subscription_deleted(data)

            elif event_type == "invoice.payment_succeeded":

                self.handle_payment_succeeded(data)

            elif event_type == "invoice.payment_failed":
    
                self.handle_payment_failed(data)

        except Exception as e:
            # Capturar erros durante o processamento
            return Response({"error": str(e)}, status=500)

        return Response({"message": "Webhook processed successfully"})

    def handle_subscription_created(self, data):

        customer_id = data.get("customer")
        subscription_id = data.get("id")
        plan = data.get("items", {}).get("data", [])[0].get("plan", {}).get("id")

        stripe_customer = stripe.Customer.retrieve(customer_id)
        customer_email = stripe_customer.get('email')

        user = User.objects.get(email=customer_email)
        get_plan = Plans.objects.get(stripe_price_id=plan)

        current_period_start = datetime.fromtimestamp(data.get("current_period_start"))
        current_period_end = datetime.fromtimestamp(data.get("current_period_end"))
        cancel_at_period_end = data.get("cancel_at_period_end", False)

        Subscription.objects.update_or_create(
            user=user,
            defaults={
                "stripe_customer_id": customer_id,
                "stripe_subscription_id": subscription_id,
                "stripe_price_id": plan,
                "plan": get_plan,
                "active": True,
                "current_period_start": current_period_start,
                "current_period_end": current_period_end,
                "cancel_at_period_end": cancel_at_period_end,
            }
        )



    def handle_subscription_updated(self, data):

        customer_id = data.get("customer")
        subscription_id = data.get("id")
        plan = data.get("items", {}).get("data", [])[0].get("plan", {}).get("id")

        status = data.get("status")

        stripe_customer = stripe.Customer.retrieve(customer_id)
        customer_email = stripe_customer.get('email')

        user = User.objects.get(email=customer_email)
        get_plan = Plans.objects.get(stripe_price_id=plan)

        current_period_start = datetime.fromtimestamp(data.get("current_period_start"))
        current_period_end = datetime.fromtimestamp(data.get("current_period_end"))
        cancel_at_period_end = data.get("cancel_at_period_end", False)

        subscription = Subscription.objects.get(user=user)

        if subscription.stripe_price_id != plan:

            print(f"Usuário {user.email} mudou de plano: {subscription.stripe_price_id} → {plan}")

            subscription.plan = get_plan 

        elif subscription.current_period_end != current_period_end:

            print(f"Usuário {user.email} renovou a assinatura.")
        
        if cancel_at_period_end:

            print(f"Usuário {user.email} cancelou a assinatura. Ela expira em {current_period_end}.")

        subscription.stripe_customer_id = customer_id
        subscription.stripe_subscription_id = subscription_id
        subscription.stripe_price_id = plan
        subscription.active = (status == "active")
        subscription.current_period_start = current_period_start
        subscription.current_period_end = current_period_end
        subscription.cancel_at_period_end = cancel_at_period_end

        subscription.save()



    def handle_subscription_deleted(self, data):

        customer_id = data.get("customer")
        subscription_id = data.get("subscription")

        plan = data.get("items", {}).get("data", [])[0].get("plan", {}).get("id")

        stripe_customer = stripe.Customer.retrieve(customer_id)
        customer_email = stripe_customer.get('email')

        user = User.objects.get(email=customer_email)

        get_plan = Plans.objects.get(pk=1)

        if subscription_id:

            Subscription.objects.filter(user=user).update(
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                stripe_price_id=plan,
                plan=get_plan,
                active=True,
            )
    
    def handle_payment_succeeded(self, data):

        customer_id = data.get("customer")
        subscription_id = data.get("subscription")

        stripe_customer = stripe.Customer.retrieve(customer_id)
        customer_email = stripe_customer.get('email')

        user = User.objects.get(email=customer_email)

        if subscription_id:

            Subscription.objects.filter(user=user).update(
                active=True,
            )


    def handle_payment_failed(self, data):

        customer_id = data.get("customer")
        subscription_id = data.get("subscription")
        items = data.get("lines", {}).get("data", [])

        if not items:

            print("Nenhum item encontrado no evento 'invoice.payment_failed'")

            return

        plan = items[0].get("price", {}).get("id")


        try:

            stripe_customer = stripe.Customer.retrieve(customer_id)
            customer_email = stripe_customer.get('email')

        except Exception as e:

            print(f"Erro ao recuperar cliente do Stripe: {e}")

            return

        try:

            user = User.objects.get(email=customer_email)

        except User.DoesNotExist:

            print(f"Usuário com o email {customer_email} não encontrado.")
            return

        try:

            get_plan = Plans.objects.get(stripe_price_id=plan)

        except Plans.DoesNotExist:

            print(f"Plano com o Stripe Price ID {plan} não encontrado.")
            return

        if subscription_id:

            Subscription.objects.filter(user=user).update(
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                stripe_price_id=plan,
                plan=get_plan,
                active=False,
            )
            print(f"Pagamento falhou para o usuário {user.email}. Assinatura desativada.")

