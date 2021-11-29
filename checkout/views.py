from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    # the payment intent 
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    # if bag is empty
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        # redirect back to the checkout page 
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    # set secret key on stripe 
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)

    # create empty instance of order form 
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51K1HPjFEToCWPRVclerd629oZ2GPMA7MZ35nvCP1MFMF3TOaGag82Zcnss3Yks7VrpnTs54aTBofqbdW71E4mX19009CY8EerJ',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)