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
    # The session allows users to add to their bag, go back and add more, without adding more before submitting their basket for payment
    # bag here accesses the request's session, and makes an empty dictionary if it doesn't exist
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        # update quantity if item is in bag
        bag[item_id] += quantity
    else:
        # add item if it's not already in bag
        bag[item_id] = quantity

    request.session['bag'] = bag
    # This print shows us what's in the bag before the functionality is added to the front end
    print(request.session['bag'])
    return redirect(redirect_url)
