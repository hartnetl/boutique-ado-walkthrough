from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # Setting this to none means you don't get an error if there is no search 
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        # check if sort is in query
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            # renaming sort to sortkey preserves the original name from being set to lower
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            # if sort is there, also check for direction
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

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


    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        # If no sorting, the below value will be 
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    # post handler
    if request.method == 'POST':
        # Instantiate a new instance of the product form from request.post and
        # include request.files to get the image of the product if one was submitted.
        form = ProductForm(request.POST, request.FILES)
        # If the form is valid, save it
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            # Error on form
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)