from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


# link to this bit
# https://youtu.be/IH0d1rLVW3s?t=364

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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

    request.session['bag'] = bag
    return redirect(redirect_url)
