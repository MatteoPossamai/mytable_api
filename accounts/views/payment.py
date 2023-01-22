from django.http.response import JsonResponse
from rest_framework import status, views
from django.shortcuts import redirect
from django.conf import settings

import json
import stripe

from mytable.settings import STRIPE_SECRET

stripe.api_key = STRIPE_SECRET


class CreateCheckoutSessionView(views.APIView):

    def post(self, request, format=None):
        try:
            prices = stripe.Price.list(
                lookup_keys=[request.data.get('lookup_key')],
                expand=['data.product']
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=settings.DOMAIN_URL +
                '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.DOMAIN_URL+ '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePortalSessionView(views.APIView):
    def post(self, request, format=None):
        checkout_session_id = request.data.get('session_id')
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        return_url = settings.DOMAIN_URL

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        return redirect(portalSession.url, code=303)


class WebhookView(views.APIView):

    def post(self, request, format=None):
        # Replace this endpoint secret with your endpoint's unique secret
        # If you are testing with the CLI, find the secret by running 'stripe listen'
        # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
        # at https://dashboard.stripe.com/webhooks
        webhook_secret = 'whsec_12345'
        request_data = json.loads(request.data)

        if webhook_secret:
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        print('event ' + event_type)

        if event_type == 'checkout.session.completed':
            print('🔔 Payment succeeded!')
        elif event_type == 'customer.subscription.trial_will_end':
            print('Subscription trial will end')
        elif event_type == 'customer.subscription.created':
            print('Subscription created %s', event.id)
        elif event_type == 'customer.subscription.updated':
            print('Subscription created %s', event.id)
        elif event_type == 'customer.subscription.deleted':
            # handle subscription canceled automatically based
            # upon your subscription settings. Or if the user cancels it.
            print('Subscription canceled: %s', event.id)

        return json.dumps({'status': 'success'})