from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
import json
from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product


# handle if user wants their details saved 
@require_POST
def cache_checkout_data(request):
    try:
        # make post request, give it the scret id, split it to get the payment intent id only
        pid = request.POST.get('client_secret').split('_secret')[0]
        # Set up stripe with the secret key to modify the payment intent
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Set up modification of pid
        stripe.PaymentIntent.modify(pid, metadata={
            # this is what we want to change: 
            # json dump of their shopping bag
            'bag': json.dumps(request.session.get('bag', {})),
            # if they want to save their info
            'save_info': request.POST.get('save_info'),
            # user placing the order
            'username': request.user,
        }) 
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
   
    # for the payment intent
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Check if the form method is post 
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        # If form is valid, save the order 
        if order_form.is_valid():
            order = order_form.save()
            # iterate through each bag item to create each line item 
            for item_id, item_data in bag.items():
                try:
                    # get product id 
                    product = Product.objects.get(id=item_id)
                    # If value is an integer it's an item without sizes 
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            # so quantity is just item data 
                            quantity=item_data,
                        )
                        order_line_item.save()
                    # if the item has sizes 
                    else:
                        # iterate through each size and create a line item accordingly 
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                # on the off chance a product isn't found 
                except Product.DoesNotExist:
                    # return error message 
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    # delete order 
                    order.delete()
                    # go back to shopping bag 
                    return redirect(reverse('view_bag'))

            # Did user want to save their info 
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            # form wasn't valid 
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
    # get request 
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

    # create empty instance of order form
        order_form = OrderForm()

    # message incase you forget to set secret key
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # check if user wanted to save their info 
    save_info = request.session.get('save_info')
    # get order created in previous view 
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # delete user's shopping bag
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
