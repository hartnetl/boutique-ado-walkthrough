from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product
# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


# link to this bit
# https://youtu.be/IH0d1rLVW3s?t=364

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)
    # get the quantity from the form and convert to string
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # The session allows users to add to their bag, go back and add more, without adding more before submitting their basket for payment
    # bag here accesses the request's session, and makes an empty dictionary if it doesn't exist
    bag = request.session.get('bag', {})

    # check if product with size is being added
    if size:
        if item_id in list(bag.keys()):
            # check for item with same size and id 
            if size in bag[item_id]['items_by_size'].keys():
                # if it does increase the quantity
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # if it doesn't then add it by the quantity wanted
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # The below allows us to structure the bag so that we can have a
            # single item id for each item but still track multiple sizes.
            bag[item_id] = {'items_by_size': {size: quantity}}
    # if no size is included
    else:
        if item_id in list(bag.keys()):
            # update quantity if item is in bag
            bag[item_id] += quantity
        else:
            # add item if it's not already in bag
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

# CI link to this 
# https://youtu.be/oQK_VSyyHRI?t=44 

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # If item has a size
        if quantity > 0:
            # If there are items, set the quantity accordingly
            bag[item_id]['items_by_size'][size] = quantity
        else:
            # otherwise remove the item
            del bag[item_id]['items_by_size'][size]
            # And remove the item id if there are no other sizes so you don't have an empty dictionary
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        # Items that don't have a size
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            # remove the size they want to remove only
            del bag[item_id]['items_by_size'][size]
            # If there are no other sizes in the bag, delete that item id so you don't have an empty items by size dictionary.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            # If there is no size, just pop it out of the bag
            bag.pop(item_id)

        request.session['bag'] = bag
        # we want a http response because it's implemented with js
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
