from django.http.response import JsonResponse
from rest_framework import generics, status, views

import os, json
import stripe

from mytable.settings import STRIPE_SECRET
from mytable.settings.constants import REDIRECT_PAGE, DOMAIN_URL

stripe.api_key = STRIPE_SECRET


class CreateCheckoutSessionView(views.APIView):

    def post(self, request, format=None):
        try:
            prices = stripe.Price.list(
                lookup_keys=[request.form['lookup_key']],
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
                success_url=DOMAIN_URL +
                '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=DOMAIN_URL + '?canceled=true',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            return "Server error", 500

class WebhookView(views.APIView):

    def post(self, request, format=None):
        # Replace this endpoint secret with your endpoint's unique secret
        # If you are testing with the CLI, find the secret by running 'stripe listen'
        # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
        # at https://dashboard.stripe.com/webhooks
        webhook_secret = 'whsec_12345'
        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
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

        return jsonify({'status': 'success'})