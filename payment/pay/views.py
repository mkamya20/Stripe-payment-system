from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'pay/home.html', context)

@csrf_exempt
def process_payment(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')  # Amount will be in cents
        name = data.get('name')  # Cardholder name
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            metadata={
                'cardholder_name': name
            }
        )

        # Create payment record
        Payment.objects.create(
            cardholder_name=name,
            amount=amount / 100,  # Convert cents to dollars
            payment_intent_id=payment_intent.id,
            status='pending'
        )

        return JsonResponse({
            'clientSecret': payment_intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

def success(request):
    # Update payment status if payment_intent_id is in the URL
    payment_intent_id = request.GET.get('payment_intent')
    if payment_intent_id:
        try:
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)
            payment.status = 'succeeded'
            payment.save()
        except Payment.DoesNotExist:
            pass
    return render(request, 'pay/success.html')
