from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    # The init method of the class is a setup method that's called every time
    # an instance of the class is created. Here we're going to use it to assign
    # the request as an attribute of the class
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        print(intent)
        # get payment id
        pid = intent.id
        # get shopping bag
        bag = intent.metadata.bag
        # get save preference
        save_info = intent.metadata.save_info

        # store all of these details 
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details:
        # replace any empty strings in the shipping details with none since 
        # stripe will store them as blank strings which is not the same as the
        # null value we want in the database.
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked

        # set profile to none so anonymous users can checkout 
        profile = None
        # get the username 
        username = intent.metadata.username
        # if username isn't anonymous, they were authenticated 
        if username != 'AnonymousUser':
            # get their profile using their username 
            profile = UserProfile.objects.get(user__username=username)
            # if the save info box is checked, we update their shipping details 
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        # Explanation of what's happening at checkout process https://youtu.be/TWeK8klQq00?t=131

        # check if order exists, and if it does return a response, if it doesn't then create it 
        # Check if order exists
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                # use info to find the order 
                order = Order.objects.get(
                    # iexact finds a case insensitive exact match 
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # If the order is found we set order exists to true
                order_exists = True
                # break out of while loop if order is found 
                break
            # increment attempt by 1 if not found  
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        # What to do if it does
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        # Now handle an order that doesn't exist
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # load the bag from json instead of the session
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()

            # If anything goes wrong, delete the order
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
