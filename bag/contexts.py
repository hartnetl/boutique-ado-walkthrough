from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """
    This is a context processor.
    Its purpose is to make this dictionary available to all templates across the entire application
    Don't forget to add this to the context processors in settings.py to make it available throughout the app
    """

    # List for the bag items to live 
    bag_items = []
    # starting total 
    total = 0
    # empty basket
    product_count = 0
    # Access the session's shopping bag
    bag = request.session.get('bag', {})

    # For each item and quantity in bag
    for item_id, item_data in bag.items():

        # execute this code if no size supplied and data is just an integer (for quantity)
        if isinstance(item_data, int):
            # Get the product
            product = get_object_or_404(Product, pk=item_id)
            # Add its quantity times the price to the total
            total += item_data * product.price
            # Increment the product count by the quantity
            product_count += item_data
            # add a dictionary to the list of bag items containing the id, quantity and the product object itself.
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

        # execute this one if size is supplied 
        else:
            product = get_object_or_404(Product, pk=item_id)
            # iterate through inner dictionary of items by size
            for size, quantity in item_data['items_by_size'].items():
                # increment items accordingly
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        # Decimal is less susceptible to rounding errors than using Float. Always use this for money
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # Let user how much more they need for free shipping
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
