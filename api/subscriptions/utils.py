import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def update_subscription_plan(subscription_id, new_price_id):
    
    try:

        subscription = stripe.Subscription.retrieve(subscription_id)

        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': new_price_id,
            }],
        )
        
        return updated_subscription
    
    except stripe.error.StripeError as e:
        print(f"Erro ao mudar de plano: {e}")
        return None
