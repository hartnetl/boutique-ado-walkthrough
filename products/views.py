from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # Setting this to none means you don't get an error if there is no search 
    query = None
    categories = None

    if request.GET:

        # check if the category exists 
        if 'category' in request.GET:
            # if it exists, split it at the commas 
            categories = request.GET['category'].split(',')
            # filter the current query to all products that have the specifed category
            # NOTEE: Using double underscores in common when making queries in django
            # Using it here means we're looking for the name field of the category model.
            products = products.filter(category__name__in=categories)
            # filter all categories down to the ones whose name is in the list from the URL.
            # Doing this turns the url strings into actual objects
            categories = Category.objects.filter(name__in=categories)

        # check if query exists 
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Q works better than product.object.filter so everything isn't and-ed together
            # This lets you search for something in product name or description 
            # READ QUERIES SECTION OF DJANGO DOCUMENTATION
            # TO USE Q: Set variable equal to Q object where the name or contains the query
            # pipe is the OR statement, i makes the query case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
