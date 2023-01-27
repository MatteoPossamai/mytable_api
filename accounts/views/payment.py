from django.http.response import JsonResponse
from rest_framework import status, views
from django.shortcuts import redirect
from django.conf import settings

import stripe
import jwt

from mytable.settings import STRIPE_SECRET
from mytable.settings import JWT_SECRET
from restaurant.models.restaurant import Restaurant
from utilities import IsLogged
from accounts.models.restaurant_user import RestaurantUser
from accounts.serializers.restaurant_user import RestaurantUserSerializer

stripe.api_key = STRIPE_SECRET


class CreateCheckoutSessionView(views.APIView):
    """
    Description: Create a checkout session for a customer
    """

    def post(self, request, format=None):
        try:
            # For now is fine sending the email, but in the future we should send the token
            email= request.data.get('customer_email')
            customer = RestaurantUser.objects.get(email=email)

            keys = request.POST.getlist('price')
            
            items = []

            for price in keys:
                items.append({
                    'price': price,
                    'quantity': 1,
                })

            checkout_session = stripe.checkout.Session.create(
                customer=customer.stripe_customer_id,
                line_items=items,
                mode='subscription',
                success_url= "http://localhost:3000/payment/" +
                '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.DOMAIN_URL+ '?canceled=true',
                subscription_data={
                    'trial_period_days': 30,
                },
            )

            print(checkout_session)
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePortalSessionView(views.APIView):
    """
    Description: Create a portal session for a customer
    """
    def post(self, request, format=None):
        checkout_session_id = request.data.get('session_id')
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        return_url = settings.DOMAIN_URL

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        return redirect(portalSession.url, code=303)


class CustomerPortalView(views.APIView):
    """
    Description: Customer portal
    """
    permission_classes = [IsLogged]

    def post(self, request, format=None):
        token = request.headers.get('token')
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = decoded['user_id']
        user = RestaurantUser.objects.get(id=user_id)

        return_url = settings.DOMAIN_URL
        customer_id = user.stripe_customer_id

        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )       
        return redirect(session.url, code=303)


class WebhookView(views.APIView):
    """
    Description: Webhook for Stripe
    """

    def post(self, request, format=None):
        # Replace this endpoint secret with your endpoint's unique secret
        # If you are testing with the CLI, find the secret by running 'stripe listen'
        # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
        # at https://dashboard.stripe.com/webhooks
        payload = request.body
        signature = request.headers.get('stripe-signature')
        endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET
        try: 
            event = stripe.Webhook.construct_event(
                payload, signature, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            print(e)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

        data = event['data']
        event_type = event['type']

        if event_type == 'checkout.session.completed':
            session = event['data']['object']

            # Fetch all the required data from session
            client_reference_id = session.get('client_reference_id')
            stripe_customer_id = session.get('customer')
            stripe_subscription_id = session.get('subscription')

            # Get the user and create a new StripeCustomer
            restaurant = Restaurant.objects.get(id=client_reference_id)
            restaurant.stripe_customer_id = stripe_customer_id
            restaurant.stripe_subscription_id = stripe_subscription_id
            restaurant.save()

        elif event_type == 'invoice.paid':
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            print(data)
        elif event_type == 'invoice.payment_failed':
            # The payment failed or the customer does not have a valid payment method.
            # The subscription becomes past_due. Notify your customer and send them to the
            # customer portal to update their payment information.
            print(data)
        else:
            print('Unhandled event type {}'.format(event_type))

        return JsonResponse({}, status=status.HTTP_200_OK)


class GetProductsView(views.APIView):
    """
    Description: Get all products
    """

    def get(self, request, format=None):
        try: 
            products = stripe.Price.list(limit=5)
            return JsonResponse(products, safe=False)
        except Exception as e:
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCustomerSubscription(views.APIView):
    """
    Description: Get customer subscription
    """
    permission_classes = [IsLogged]

    def get(self, request, format=None):
        try: 
            token = request.headers.get('token')
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = decoded['user_id']
            user = RestaurantUser.objects.get(id=user_id)
            customer_id = user.stripe_customer_id

            # Get the subscription
            subscription = stripe.Subscription.list(customer=customer_id)

            valid_subscription = []
            for sub in subscription.data:
                if sub.status == 'active' or sub.status == 'trialing' or sub.status == 'incomplete_expired':
                    valid_subscription.append(sub)

            return JsonResponse({"data":valid_subscription, "number": len(valid_subscription)}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

