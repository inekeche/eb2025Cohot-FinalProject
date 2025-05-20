#Add these to INSTALLED_APPS in agri_api/settings.py:


INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    'users',
    'products',
    'orders',
]


#Add middleware for CORS if frontend is separate:


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True


#JWT Authentication Setup


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}




#Generate the models, serializers, and basic APIs for the following apps:


#users App – User Authentication

#users/models.py
#Using Django’s built-in AbstractUser:

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    def __str__(self):
        return self.username


#users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_farmer', 'is_supplier')



#Stripe Payment Integration — Backend Setup
#Install Stripe Python SDK

#pip install stripe
#Add Stripe settings to agri_api/settings.py

import os

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'your_test_secret_key')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'your_test_publishable_key')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'your_webhook_secret')
#(Make sure to create environment variables in your deployment setup.)

#Create Stripe Checkout Session API
#In your orders/views.py add:

import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    user = request.user
    data = request.data  # expected: { items: [{ product: id, quantity: n }, ...] }

    try:
        # Create Order first
        order = Order.objects.create(user=user, is_paid=False, total_price=0)
        total_amount = 0

        line_items = []

        for item in data.get('items', []):
            product = Product.objects.get(id=item['product'])
            quantity = int(item['quantity'])
            price_cents = int(product.price * 100)  # Stripe requires cents

            # Create order items
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            total_amount += product.price * quantity

            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': price_cents,
                },
                'quantity': quantity,
            })

        order.total_price = total_amount
        order.save()

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/cancel',
            client_reference_id=str(order.id),
            customer_email=user.email,
        )

        return Response({'id': session.id})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#Add Webhook to Confirm Payment

#Create a webhook view in orders/views.py:


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order_id = session.get('client_reference_id')
        try:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.save()

            # Decrease stock for each order item
            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)




#Add URLs to orders/urls.py

from django.urls import path
from .views import create_checkout_session, stripe_webhook

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]



#Include orders.urls in main agri_api/urls.py

path('api/orders/', include('orders.urls')),