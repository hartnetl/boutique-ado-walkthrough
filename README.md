![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Walkthrough steps

- [Workspace setup](#set-up-your-workspace)  
- [Authentication](#allauth-authentication)
- [Base template setup](#setup-base-template)
- [Home page template setup](#home-setup)
- [Products setup](#product-setup)
- [Products filtering and search](#product-filtering-and-search)
- [Product sorting](#product-sorting)
- [Shopping bag](#shopping-bag)
- [Add products to bag](#adding-products-to-bag)
- [Adjusting quantity of items in bag](#adjusting-quantity-of-items-in-bag)
- [Toasts](#toasts)
- [Checkout app](#checkout-app)
- [Stripe payments](#stripe-payments)
- [Profile app](#profile-app)
- [Product Admin](#product-admin)
- [Deploy to heroku](#deploy-to-heroku)
- [Sending emails with Django](#sending-emails)
- [Code Refactoring](#code-refactoring)

##

<details>
<summary></summary>

[Back to top](#walkthrough-steps)
</details>


## Set up your workspace

<details>
<summary>Click me</summary>

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/ae8231be6e7c43b8afef428525ff7420/?child=first)

        pip3 install django

    Create the project 

        django-admin startproject boutique_ado .
    
    Add necessary files to gitignore 
    Test it works

        python3 manage.py runserver

    Make your migrations

        python3 manage.py migrate

    Create a superuser

        python3 manage.py createsuperuser

[Back to top](#walkthrough-steps)

</details>

<hr>

## Allauth authentication

<details>
<summary>click here</summary>

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/4df834ab921c418aa40b1b73ae878d0e/?child=first)
[allauth documantation](https://django-allauth.readthedocs.io/en/latest/installation.html)

**Note** Use this version of allauth for the followalong:    pip3 install django-allauth==0.41.0  
Also ensure os is imported at the top of the settings.py file automatically

First handle the registration and user accounts user stories as it's fundamental to any account.

Install allauth 

        pip3 install django-allauth==0.41.0  

Head to the allauth docs and add in your required settings to settings.py  
Note: This walkthrough doesn't use socials sign in; learn how to do this

Add allauth URL to urls.py

        path('accounts/', include('allauth.urls')),

    Import include from django.urls

Run migrations again

    python3 manage.py migrate

Open server 

    python3 manage.py runserver

Go to admin panel (/admin) and sign in with your superuser details

    Go to sites  
    Change your example site  
        Domain name: boutiqueado.example.com  
        Display name: Boutique Ado

    This is essential for social sign in


**Important!:**   
When trying to send actual emails from Gitpod, an error stating Issue binding port will be displayed which causes sending of the email to fail. Logging issues to the terminal while developing on Gitpod, as done in this video, serves to test Authentication and Authorisation functionality until project deployment.

Once deployed to Heroku, the sending of actual emails will become a possibility, so please wait until then before attempting it.


Set up allauth settings - settings.py

    allauth is going to send confirmation emails when an account is created, so we're going to temporarily log them to the console
    
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    allauth settings

        ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
        ACCOUNT_EMAIL_REQUIRED = True
        ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
        ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
        ACCOUNT_USERNAME_MIN_LENGTH = 4

    where to go to login
    
        LOGIN_URL = '/accounts/login/'
    
    where to go after you've logged in
    
        LOGIN_REDIRECT_URL = '/success'


Test it worked

    python3 manage.py runserver

    yoururl /accounts/login

    sign in 
    you'll get redirected to confirm-email

    go to admin panel
    email-address model
    add an email address to your account and set as primary and verified

    logout
    login through accounts/login
    You'll get a 404 page error because it redirects to /success like we told it to in settings.py 
    Now go to that redirect and change it from /success to just /

Save your requirements

    pip3 freeze > requirements.txt

Set up your templates directory

    mkdir templates
    mkdir templates/allauth

[Back to top](#walkthrough-steps)

</details>

<hr>

## Setup base template
<details>
<summary>Click me</summary>

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/fd5e6b796c0045358567707d02060317/?child=first)  
[bootstrap starter code (v4.4)](https://getbootstrap.com/docs/4.4/getting-started/introduction/#starter-template)

**Note** For this project use the **minified** version of jQuery

Copy the allauth template files into your newly made directory

    cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth

Delete the openid and test folders - they will then revert to default allauth versions  
Create base.html file in templates  
Copy bootstrap starter template (linked above)

Edit starter template. Wrap code in jinja blocks - {% block meta %}, {% block corecss %}, {% block corejs %}  
Add 3 extra blocks for extra versions of each  
Inside the title add a {% block extra_title%}

Add basic template to the body

    <body>
   
    <header class="container-fluid fixed-top"></header>

    {% if messages %}
    <div class="message-container"></div>
    {% endif %}
    
    {% block page_header %}
    {% endblock %}

    {% block content %}
    {% endblock %}

    {% block postloadjs %}
    {% endblock %}

    </body>


Create home app

    python3 manage.py startapp home

Create templates folder in the home app 

    mkdir -p home/templates/home

Create index.html file in the home template folder and fill with test code

    {% extends "base.html" %}
    {% load static %}

    {% block content %}

    <h1 class="display-4 text-success">It works!</h1>
    {% endblock %}

Create view to render the code (home/views.py)

    def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

Create urls.py file inside home folder

    from django.contrib import admin
    from django.urls import path, include
    from . import views

    urlpatterns = [
    path('', views.index, name='home'),
    ]

Go to urls.py inside boutique_ado

    Add this path
        path('', include('home.urls')),

Add home app to settings.py installed apps

After that add in the template directories

    'DIRS': [
            # Add route and custom allauth templates directory
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],

Test it worked 

    python3 manage.py runserver
    You should have a page saying "It works" as per your index.html code


[Back to top](#walkthrough-steps)

</details>

<hr>

## Home setup

<details>
<summary>click me here</summary>

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/196e74d3dd5849cd801d319d7095c3eb/?child=first)

<details>
<summary>Video 1</summary>

Structure the homepage template

        {% extends "base.html" %}
        {% load static %}

        {% block page_header %}
            <div class="container header-container">
                <div class="row">
                    <div class="col">
                        
                    </div>
                </div>
            </div>
        {% endblock %}


        {% block content %}

        <h1 class="display-4 text-success">It works!</h1>
        <!-- h-100 gives 100% height (container and row) and my-auto (column) for vertical centering -->
            <div class="container h-100">
                <div class="row h-100">
                    <!-- make the column sit to the left -->
                    <div class="col-7 col-md-6 my-auto">
                        <!-- display-4 is a bootstrap heading class; logo-font and text-black will be manual css -->
                        <h1 class="display-4 logo-font text-black">The new collections are here!</h1>
                        <div class="my-5">
                            <h4>
                                <a href="" class="shop-now-button btn btn-lg rounded-0 text-uppercase py-3">Shop Now</a>
                            </h4>
                        </div>
                    </div>
                </div>
            </div>
        {% endblock %}

Add structure to the base.html header

        <header class="container-fluid fixed-top">
        <div class="row">
        <!-- A single row with 3 columns which stack vertically on everything except large and up screens 
            The columns are centered with extra padding for smaller screens -->

        <!-- logo  -->
        <!-- The logo should be centred, but left aligned on large and up screens  -->
        <div class="col-12 col-lg-4 my-auto py-1 py-lg-0 text-center text-lg-left">
            <a href="{% url 'home' %}" class="nav-link main-logo-link">
            <h2 class="logo-font text-black my-0"><strong>Boutique </strong>Ado</h2>
            </a>
        </div>

        <!-- Search bar  -->
        <div class="col-12 col-lg-4 my-auto py-1 py-lg-0">
            <form method="GET" action="">
            <div class="input-group w-100">
                <!-- This input is a type bar; q is for query -->
                <input class="form-control border border-black rounded-0" type="text" name="q"
                placeholder="Search our site">
                <!-- This input-group-append is a bootstrap class to attach button to text input -->
                <div class="input-group-append">
                <!-- button for submitting  -->
                <button class="form-control btn btn-black border border-black rounded-0" type="submit">
                    <span class="icon">
                    <i class="fas fa-search"></i>
                    </span>
                </button>
                </div>
            </div>
            </form>
        </div>

        <!-- account and shopping bag links  -->
        <div class="col-12 col-lg-4 my-auto py-1 py-lg-0">
            <!-- these ul classes align list horizontally with no bullets  -->
            <ul class="list-inline list-unstyled text-center tetx-lg-right my-0">
            <li class="list-inline-item dropdown"></li>
            <li class="list-inline-item"></li>
            </ul>
        </div>
        </div>
    </header>

</details>

<details>
<summary>Video 2</summary>

Add to account and shopping bag links in base.html

         <!-- account and shopping bag links  -->
        <div class="col-12 col-lg-4 my-auto py-1 py-lg-0">
            <!-- these ul classes align list horizontally with no bullets  -->
            <ul class="list-inline list-unstyled text-center tetx-lg-right my-0">

            <!-- dropdown menu  -->
            <li class="list-inline-item dropdown">
                <!-- This is the parent menu containing a dropdown menu with user icon  -->
                <a class="text-black nav-link" href="#" id="user-options" data-toggle="dropdown" aria-haspopup="true"
                aria-expanded="false">
                <div class="text-center">
                    <div><i class="fas fa-user fa-lg"></i></div>
                    <p class="my-0">My Account</p>
                </div>
                </a>

                <!-- This is what gets displayed in the dropdown menu  -->
                <div class="dropdown-menu border-0" aria-labelledby="user-options">
                {% if request.user.is_authenticated %}
                    {% if request.user.is_superuser %}
                        <a href="" class="dropdown-item">Product Management</a>
                    {% endif %}
                        <a href="" class="dropdown-item">My Profile</a>
                        <!-- These account urls come from allauth  -->
                        <a href="{% url 'account_logout' %}" class="dropdown-item">Logout</a>
                {% else %}
                    <a href="{% url 'account_signup' %}" class="dropdown-item">Register</a>
                    <a href="{% url 'account_login' %}" class="dropdown-item">Login</a>
                {% endif %}
                </div>
            </li>

            <!-- Shopping bag link  -->
            <li class="list-inline-item">
                <a class="{% if grand_total %}text-info font-weight-bold{% else %}text-black{% endif %} nav-link" href="">
                <div class="text-center">
                    <div><i class="fas fa-shopping-bag fa-lg"></i></div>
                    <p class="my-0">
                    {% if grand_total %}
                        ${{ grand_total|floatformat:2 }}
                    {% else %}
                        $0.00
                    {% endif %}
                    </p>
                </div>
                </a>
            </li>
            </ul>
        </div>
        </div>

Start the css

</details>

<details>
<summary>Video 3</summary>

[fontawesome](https://fontawesome.com/kits/a7bc66b529/use)  

Get lato fonts from google and load them into core css  
Link custom css "base.css" to corecss  
Go to fontawesome - account - kits - copy your link  
    Paste that into your corejs  

In settings.py under static_url at the bottom, tell django where the static files are located

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

Under that tell it where the uploaded media files will go

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Go to project urls.py and add hte media url from settings

    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('allauth.urls')),
        path('', include('home.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

</details>

<details>
<summary>Video 4 - navigation</summary>


Create includes folder in templates (for small codes of html)  
Put two files in this: main-nav.html and mobile-top-header.html  

<details>
<summary>Create html for mobile top header</summary>

        <li class="list-inline-item">
            <a class="text-black nav-link d-block d-lg-none" href="#" id="mobile-search" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <div class="text-center">
                    <div><i class="fas fa-search fa-lg"></i></div>
                    <p class="my-0">Search</p>
                </div>
            </a>
            <div class="dropdown-menu border-0 w-100 p-3 rounded-0 my-0" aria-labelledby="mobile-search">
                <form class="form" method="GET" action="">
                    <div class="input-group w-100">
                        <input class="form-control border border-black rounded-0" type="text" name="q" placeholder="Search our site">
                        <div class="input-group-append">
                            <button class="form-control form-control btn btn-black border border-black rounded-0" type="submit">
                                <span class="icon">
                                    <i class="fas fa-search"></i>
                                </span>
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </li>
        <li class="list-inline-item dropdown">
            <a class="text-black nav-link d-block d-lg-none" href="#" id="user-options" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <div class="text-center">
                    <div><i class="fas fa-user fa-lg"></i></div>
                    <p class="my-0">My Account</p>
                </div>
            </a>
            <div class="dropdown-menu border-0" aria-labelledby="user-options">
                {% if request.user.is_authenticated %}
                    {% if request.user.is_superuser %}
                        <a href="{% url 'account_logout' %}" class="dropdown-item">Product Management</a>
                    {% endif %}
                    <a href="{% url 'profile' %}" class="dropdown-item">My Profile</a>
                    <a href="{% url 'account_logout' %}" class="dropdown-item">Logout</a>
                {% else %}
                    <a href="{% url 'account_signup' %}" class="dropdown-item">Register</a>
                    <a href="{% url 'account_login' %}" class="dropdown-item">Login</a>
                {% endif %}
            </div>
        </li>
        <li class="list-inline-item">
            <a class="{% if grand_total %}text-primary font-weight-bold{% else %}text-black{% endif %} nav-link d-block d-lg-none" href="">
                <div class="text-center">
                    <div><i class="fas fa-shopping-bag fa-lg"></i></div>
                    <p class="my-0">
                        {% if grand_total %}
                            ${{ grand_total|floatformat:2 }}
                        {% else %}
                            $0.00
                        {% endif %}
                    </p>
                </div>
            </a>
        </li>

</details>

<details>
<summary>Create html for main-nav </summary>

        <!-- the main-nav id matches the id of the toggle button in the base templates  -->
        <div class="collapse navbar-collapse" id="main-nav">
            <ul class="navbar-nav w-auto mx-auto">

                <!-- All products dropdown menu  -->

                <li class="nav-item dropdown">
                    <a class="logo-font font-weight-bold nav-link text-black mr-5" href="#" id="all-products-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        All Products
                    </a>
                    <div class="dropdown-menu border-0" aria-labelledby="all-products-link">
                        <a href="" class="dropdown-item">By Price</a>
                        <a href="" class="dropdown-item ">By Rating</a>
                        <a href="" class="dropdown-item ">By Category</a>
                        <a href="" class="dropdown-item">All Products</a>
                    </div>
                </li>

                <!-- Clothing dropdown menu  -->


                <li class="nav-item dropdown">
                    <a class="logo-font font-weight-bold nav-link text-black mr-5" href="#" id="clothing-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Clothing
                    </a>
                    <div class="dropdown-menu border-0" aria-labelledby="clothing-link">
                        <a href="" class="dropdown-item">Activewear &amp; Essentials</a>
                        <a href="" class="dropdown-item">Jeans</a>
                        <a href="" class="dropdown-item">Shirts</a>
                        <a href="" class="dropdown-item">All Clothing</a>
                    </div>
                </li>

                <!-- Homeware dropdown menu  -->

                <li class="nav-item dropdown">
                    <a class="logo-font font-weight-bold nav-link text-black mr-5" href="#" id="homeware-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Homeware
                    </a>
                    <div class="dropdown-menu border-0" aria-labelledby="homeware-link">
                        <a href="" class="dropdown-item">Bed &amp; Bath</a>
                        <a href="" class="dropdown-item">Kitchen &amp; Dining</a>
                        <a href="" class="dropdown-item">All Homeware</a>
                    </div>
                </li>

                <!-- special offers dropdown menu  -->

                <li class="nav-item dropdown">
                    <a class="logo-font font-weight-bold nav-link text-black" href="#" id="specials-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Special Offers
                    </a>
                    <div class="dropdown-menu border-0" aria-labelledby="specials-link">
                        <a href="" class="dropdown-item">New Arrivals</a>
                        <a href="" class="dropdown-item">Deals</a>
                        <a href="" class="dropdown-item">Clearance</a>
                        <a href="" class="dropdown-item">All Specials</a>
                    </div>
                </li>
            </ul>
        </div>
</details>


Now add these two to base.html

Create a div underneath the div with id 'topnav' in the header 

        <div class="row bg-white">
            <nav class="navbar navbar-expand-lg navbar-light w-100">
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#main-nav"
                aria-controls="main-nav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                {% include 'includes/mobile-top-header.html' %}
                {% include 'includes/main-nav.html' %}
            </nav>
        </div>
        <div id="delivery-banner" class="row text-center">
            <div class="col bg-black text-white">
                <h4 class="logo-font my-1">Free delivery on orders over ${{ free_shipping_threshold }}!</h4>
            </div>
        </div>

</details>

[Back to top](#walkthrough-steps)

</details>

<hr>

## Product setup

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/ff6e359891a240a0b92f16bf68d4851a/?child=first)

<details>
<summary>Click me</summary>


<details>
<summary>Video 1 - Adding products</summary>

[image and fixtures](https://github.com/Code-Institute-Solutions/boutique_ado_images)
**Note:**  In this video, we create the data in the database by uploading pre-written data from a file using fixtures.
It is important to mention that this is not the only way to add data to your database. When you come to build your own project, if you do not have a file of data to load up, you can manually add your database entries into the database via the admin panel.
<hr>

Load in images to media folder - sourced from kaggle.com - from the images folder linked above  

Create products app 

    python3 manage.py startapp products

Add products to installed apps in settings.py

Create fixtures folder in products folder  
Fixtures are used to load data very quickly into a django database so we don't have to do it all manually in the admin.   
They are in the form of json files in this project  

Add the category and products fixtures supplied in the link above to the fixtures folder

    Example of product json entry

        {
        "pk": 1,
        "model": "products.product",
    // These are the value for each field in the model 
        "fields": {
            "sku": "pp5001340155",
            "name": "Arizona Original Bootcut Jeans",
            "description": "Bootcut jeans in our just-right original fit are comfortable and look great too.  5-pocket style sits below waist straight fit through seat and thigh bootcut leg 18\" leg opening cotton washable imported extended sizes and washes available online only",
            "has_sizes": true,
            "price": 53.99,
        // This category value refers to the primary key (pk) of one of the categories in the other fixture file. 
            "category": 6,
            "rating": 4.6,
            "image_url": "http://s7d9.scene7.com/is/image/JCPenney/DP0709201205510679M.tif?hei=380&amp;wid=380&op_usm=.4,.8,0,0&resmode=sharp2&op_usm=1.5,.8,0,0&resmode=sharp",
            "image": "DP0709201205510679M.jpg"
        }
    },


Create models for category and product

* go to models.py in products app

        from django.db import models

        class Category(models.Model):
            # programmatic name 
            name = models.CharField(max_length=254)
            # front end name 
            friendly_name = models.CharField(max_length=254, null=True, blank=True)

            def __str__(self):
                return self.name

            def get_friendly_name(self):
                return self.friendly_name

        class Product(models.Model):
            category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
            sku = models.CharField(max_length=254, null=True, blank=True)
            name = models.CharField(max_length=254)
            description = models.TextField()
            price = models.DecimalField(max_digits=6, decimal_places=2)
            rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
            image_url = models.URLField(max_length=1024, null=True, blank=True)
            image = models.ImageField(null=True, blank=True)

            def __str__(self):
                return self.name

* Do dry run of migrations

        python3 manage.py makemigrations --dry-run

    * We need Pillow, so let's install that 

            pip3 install pillow

    * Run migrations dry run again
    * Run migrations

            python3 manage.py makemigrations 

    * Run migrate with plan flag

            python3 manage.py migrate --plan

    * Migrate

            python3 manage.py migrate

* Head to products/admin.py to register the two models to the admin panel

        from django.contrib import admin
        from .models import Product, Category

        admin.site.register(Product)
        admin.site.register(Category)

Now we need to apply fixtures to models

        python3 manage.py loaddata categories
        python3 manage.py loaddata products

        **note** In the walkthrough this worked fine. In mine I got this error  
        django.core.exceptions.FieldDoesNotExist: Product has no field named 'has_sizes'  
        So I added 'has_sizes' to the models with default set to true. ran migrations then ran the loaddate for products again and it worked.  


Run your site and check the products show up in the admin panel 


</details>


<details>
<summary>Video 2 - Products admin and views</summary>

**CUSTOMISE ADMIN**

Go to your admin panel and check how everything looks
* We want to change categorys to categories, show the friendly name of categpry and add have more fields in the products admin

products/models.py
* Under the category model add this to meta data

        class Meta:
            verbose_name_plural = 'Categories'

products/admin.py
* Add in how you want your admin panel to display your models

        from django.contrib import admin
        from .models import Product, Category


        class ProductAdmin(admin.ModelAdmin):
            list_display = (
                'sku',
                'name',
                'category',
                'price',
                'rating',
                'image',
            )

            ordering = ('sku',)


        class CategoryAdmin(admin.ModelAdmin):
            list_display = (
                'friendly_name',
                'name',
            )


        admin.site.register(Product, ProductAdmin)
        admin.site.register(Category, CategoryAdmin)


**CREATE VIEWS**

products/views.py - create the view to view all products

        from django.shortcuts import render
        from .models import Product


        def all_products(request):
            """ A view to show all products, including sorting and search queries """

            products = Product.objects.all()

            context = {
                'products': products,
            }

            return render(request, 'products/products.html', context)

products/urls.py - create url for your products view

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.all_products, name='products')
        ]

    * Note: We can remove admin from our app urls.py

boutique_ado/urls - add your allproducts url

        path('products/', include('products.urls')),

Create templates

        mkdir -p products/templates/products

    * Create products.html inside this new directory

            {% extends "base.html" %}
            {% load static %}

            {% block page_header %}
                <div class="container header-container">
                    <div class="row">
                        <div class="col">
                            
                        </div>
                    </div>
                </div>
            {% endblock %}


            {% block content %}

                <div class="container">
                    <div class="row">
                        <div class="col">
                            {{ products }}
                        </div>
                    </div>
                </div>
            {% endblock %}


</details>

<details>
<summary>Video 3 - Products template </summary>

products/templates/products.html

<details>
<summary>Click to reveal html file</summary>

        {% extends "base.html" %}
        {% load static %}

        {% block page_header %}
            <div class="container header-container">
                <div class="row">
                    <div class="col"></div>
                </div>
            </div>
        {% endblock %}

        {% block content %}
            <!-- This overlay is to coverup the background image in the homepage -->
            <div class="overlay"></div>

            <!-- This container has two rows: One to contain the page title and any currently selected categories and one for the products themselves.  -->
            <div class="container-fluid">

                <!-- Header row  -->

                <div class="row">
                    <div class="col text-center mt-3">
                        <h2 class="logo-font">Products</h2>
                        <hr class="w-50 mb-1">
                    </div>
                </div>

                <!-- Products row  -->
                <div class="row">
                    <!-- This row has 2 rows  -->
                    <div class="product-container col-10 offset-1">
                        <div class="row mt-1 mb-2"></div>

                        <!-- row 2 - products  -->

                        <div class="row">
                            {% for product in products %}
                                <div class="col-sm-6 col-md-6 col-lg-4 col-xl-3">
                                    <div class="card h-100 border-0">
                                        {% if product.image %}
                                        <a href="">
                                            <img class="card-img-top img-fluid" src="{{ product.image.url }}" alt="{{ product.name }}">
                                        </a>
                                        {% else %}
                                        <a href="">
                                            <img class="card-img-top img-fluid" src="{{ MEDIA_URL }}noimage.png" alt="{{ product.name }}">
                                        </a>
                                        {% endif %}
                                        <div class="card-body pb-0">
                                            <p class="mb-0">{{ product.name }}</p>
                                        </div>
                                        <div class="card-footer bg-white pt-0 border-0 text-left">
                                            <div class="row">
                                                <div class="col">
                                                    <p class="lead mb-0 text-left font-weight-bold">${{ product.price }}</p>
                                                    {% if product.rating %}
                                                        <small class="text-muted"><i class="fas fa-star mr-1"></i>{{ product.rating }} / 5</small>
                                                    {% else %}
                                                        <small class="text-muted">No Rating</small>
                                                    {% endif %}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- This sets the size of the hr, depending on how many columns are there  -->
                                
                                {% if forloop.counter|divisibleby:1 %}
                                    <div class="col-12 d-sm-none mb-5">
                                        <hr>
                                    </div>
                                {% endif %}                        
                                {% if forloop.counter|divisibleby:2 %}
                                    <div class="col-12 d-none d-sm-block d-md-block d-lg-none mb-5">
                                        <hr>
                                    </div>
                                {% endif %}
                                {% if forloop.counter|divisibleby:3 %}
                                    <div class="col-12 d-none d-lg-block d-xl-none mb-5">
                                        <hr>
                                    </div>
                                {% endif %}
                                {% if forloop.counter|divisibleby:4 %}
                                    <div class="col-12 d-none d-xl-block mb-5">
                                        <hr>
                                    </div>
                                {% endif %}
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        {% endblock %}

</details>

Go to base.css and add overlay css

        .overlay {
            height: 100%;
            width: 100%;
            top: 0;
            left: 0;
            position: fixed;
            background: white;
            /* -1 makes it sit behind the content  */
            z-index: -1;
        }
    
    * This will probably be used on most of the other pages


</details>

<details>
<summary>Video 4 - Products detail</summary>

Add url to products page in includes/main-nav and home/templates/home  

Create product detail view in products/views.py

        def product_detail(request, product_id):
        """ A view to show individual product details """

        product = get_object_or_404(Product, pk=product_id)

        context = {
            'product': product,
        }

        return render(request, 'products/product_detail.html', context)

Create url for the product detail view in products/url

        path('<product_id>', views.product_detail, name='product_detail'),


Create template for the view 

<detail>
<summary>Reveal template</summary>

        {% extends "base.html" %}
        {% load static %}

        {% block page_header %}
            <div class="container header-container">
                <div class="row">
                    <div class="col"></div>
                </div>
            </div>
        {% endblock %}

        {% block content %}
            <div class="overlay"></div>
            <div class="container-fluid">
                <!-- one row split into two columns  -->
                <div class="row">

                    <!-- col 1: product image  -->

                    <!-- offsetting pushes cols to the middle  -->
                    <div class="col-12 col-md-6 col-lg-4 offset-lg-2">
                        <div class="image-container my-5">
                            {% if product.image %}
                                <a href="{{ product.image.url }}" target="_blank">
                                    <img class="card-img-top img-fluid" src="{{ product.image.url }}" alt="{{ product.name }}">
                                </a>
                                {% else %}
                                <a href="">
                                    <img class="card-img-top img-fluid" src="{{ MEDIA_URL }}noimage.png" alt="{{ product.name }}">
                                </a>
                            {% endif %}
                        </div>
                    </div>

                    <!-- col 2: product info  -->
                    
                    <div class="col-12 col-md-6 col-lg-4">
                        <div class="product-details-container mb-5 mt-md-5">
                            <p class="mb-0">{{ product.name }}</p>
                            <p class="lead mb-0 text-left font-weight-bold">${{ product.price }}</p>
                            {% if product.rating %}
                                <small class="text-muted"><i class="fas fa-star mr-1"></i>{{ product.rating }} / 5</small>
                            {% else %}
                                <small class="text-muted">No Rating</small>
                            {% endif %}
                            <p class="mt-3">{{ product.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        {% endblock %}

</detail>

Fill in url product detail to each product in products.html

        {% url 'product_detail' product.id %}


Check it all works - and it should

But in mobiles the header isn't pushing down the product cards. Let's add a media query for that now

        /* pad the top a bit when navbar is collapsed on mobile */
        @media (max-width: 991px) {
            .header-container {
                padding-top: 116px;
            }

            body {
                height: calc(100vh - 116px);
            }
        }

</details>

[Back to top](#walkthrough-steps)
</details>

<hr>

## Product filtering and search

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/0fb892bc636a44cf94b69d9f2aa9166a/?child=first)

<details>
<summary>part 1 - create search function</summary>


Add action to search bar in base.html and mobile-top-heder

        {% url 'products' %}

Update all_products view to add functionality to search bar get request

        from django.shortcuts import render, get_object_or_404, redirect, reverse
        from django.contrib import messages
        from django.db.models import Q
        from .models import Product


        def all_products(request):
            """ A view to show all products, including sorting and search queries """

            products = Product.objects.all()
            query = none

            if request.GET:
                if 'q' in request.GET:
                    query = request.GET['q']
                    if not query:
                        messages.error(request, "You didn't enter any search criteria!")
                        return redirect(reverse('products'))
                    
                # query can appear in name or description. Pipe is or. i makes it case insensitive 
                    queries = Q(name__icontains=query) | Q(description__icontains=query)
                    products = products.filter(queries)

            context = {
                'products': products,
                'search_term' query,
            }

            return render(request, 'products/products.html', context)


        def product_detail(request, product_id):
            """ A view to show individual product details """

            product = get_object_or_404(Product, pk=product_id)

            context = {
                'product': product,
            }

            return render(request, 'products/product_detail.html', context)
            

    * Q is a great way to handle queries - it allows for searches to get results for names or descriptions.  
    * Using filters would mean it would have to appear in both to get a hit


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>part 2 - searching by category</summary>
<br>

- Create links to the categories in main-nav.html

            <li class="nav-item dropdown">
                <a class="logo-font font-weight-bold nav-link text-black mr-5" href="#" id="clothing-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Clothing
                </a>
                <div class="dropdown-menu border-0" aria-labelledby="clothing-link">

                <!-- 
                The links first point to the products URL. Then a question mark to indicate we're about to pass the category parameter.
                Followed by activewear and essentials separated by a comma. This syntax ensures we end up with a comma-separated string in the view. 
                -->

                    <a href="{% url 'products' %}?category=activewear,essentials" class="dropdown-item">Activewear &amp; Essentials</a>
                    <a href="{% url 'products' %}?category=jeans" class="dropdown-item">Jeans</a>
                    <a href="{% url 'products' %}?category=shirts" class="dropdown-item">Shirts</a>
                    <a href="{% url 'products' %}?category=activewear,essentials,jeans,shirts" class="dropdown-item">All Clothing</a>
                </div>
            </li>

Go to products/views.py to alter the all_products view

- set category to none

        categories = None

- Check if the category search exists

        if request.GET:
            if 'category' in request.GET:
                # if it exists, split it at the commas 
                categories = request.GET['category'].split(',')
                # filter the current query to all products that have the specifed category
                # NOTEE: Using double underscores in common when making queries in django
                # Using it here means we're looking for the name field of the category model.
                products = products.filter(category__name__in=categories)

- import Category from models to display them to the user

        from .models import Product, Category

- Filter by categories whose names are in the url

        categories = Category.objects.filter(name__in=categories)

    Doing this turns the url strings into actual objects

- Add current categories to context to be used by the template later

          context = {
                'products': products,
                'search_term': query,
                'current_categories': categories,
            }


All filtering for clothing categories should work

Apply the same url logic to all other categories on the page (main-nav.html)

[Back to top](#walkthrough-steps)
</details>

<hr>

## Product sorting

[CI videos](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/a66216c1383941c4897921a732f59237/?child=first)

<details>
<summary>PART 1 - filter by price, rating and category</summary>

<br>

Add filtering urls to main nav.html

        <li class="nav-item dropdown">
            <a class="logo-font font-weight-bold nav-link text-black mr-5" href="#" id="all-products-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                All Products
            </a>
            <div class="dropdown-menu border-0" aria-labelledby="all-products-link">
                <!-- sort price in ascending order  -->
                <a href="{% url 'products' %}?sort=price&direction=asc" class="dropdown-item">By Price</a>
                <!-- sort rating in descending order  -->
                <a href="{% url 'products' %}?sort=rating&direction=desc" class="dropdown-item ">By Rating</a>
                <a href="{% url 'products' %}?sort=category&direction=asc" class="dropdown-item ">By Category</a>
                <a href="{% url 'products' %}" class="dropdown-item">All Products</a>
            </div>
        </li>


Alter the all_products view to include this

- import Lower 

        from django.db.models.functions import Lower

- set sort and direction to none

        sort = None
        direction = None

- Check if sort in query. If it is then sort the items (using a renamed variable called sortkey)
    - If it is, we also check if there is a direction. If it's listed as desc, reverse the order of sortkey
    - If there is no direction specified, list them in regular order

            if request.GET:

                # check if sort is in query
                if 'sort' in request.GET:
                    sortkey = request.GET['sort']
                    # renaming sort to sortkey preserves the original name from being set to lower
                    sort = sortkey
                    if sortkey == 'name':
                        sortkey = 'lower_name'
                        products = products.annotate(lower_name=Lower('name'))

                    # if sort is there, also check for direction
                    if 'direction' in request.GET:
                        direction = request.GET['direction']
                        if direction == 'desc':
                            sortkey = f'-{sortkey}'
                    products = products.order_by(sortkey)

- Return the current sorting methodology to the template

        current_sorting = f'{sort}_{direction}'

- Add sorting to context

        context = {
            'products': products,
            'search_term': query,
            'current_categories': categories,
            'current_sorting': current_sorting,
        }

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 2 - get filter categories working </summary>

Add the category to each individual product card and make it a link to the actual category

- products/templates/products.html
    - Add category if statement above rating if statement

            {% if product.category %}
                <p class="small mt-1 mb-0">
                    <a class="text-muted" href="{% url 'products' %}?category={{ product.category.name }}">
                        <i class="fas fa-tag mr-1"></i>{{ product.category.friendly_name }}
                    </a>
                </p>
            {% endif %}

- Add it to products/templates/product_detail.html too in the same place above ratings
- Create category links under the products header of products.html

        {% for c in current_categories %}
            <a class="category-badge text-decoration-none" href="{% url 'products' %}?category={{ c.name }}">
                <span class="p-2 mt-2 badge badge-white text-black rounded-0 border border-dark">{{ c.friendly_name }}</span>
            </a>
        {% endfor %}

- Pop sort functionality above the list of products 

        <!-- row 1 - sort options  -->
            <div class="row mt-1 mb-2">
                <div class="product-container col-10 offset-1">
                    <div class="row mt-1 mb-2">
                        <!-- sort select is on top on mobile, but last for medium + screens  -->
                        <div class="col-12 col-md-6 my-auto order-md-last d-flex justify-content-center justify-content-md-end">
                            <!-- sort select box  -->
                            <div class="sort-select-wrapper w-50">
                                <select id="sort-selector" class="custom-select custom-select-sm rounded-0 border border-{% if current_sorting != 'None_None' %}info{% else %}black{% endif %}">
                                    <!-- Here we're checking the current_sorting returned by the view to determine which option was selected  -->
                                    <!-- JS is used to make this box work  -->
                                    <option value="reset" {% if current_sorting == 'None_None' %}selected{% endif %}>
                                        Sort by...</option>
                                    <option value="price_asc"
                                        {% if current_sorting == 'price_asc' %}selected{% endif %}>Price (low to high)
                                    </option>
                                    <option value="price_desc"
                                        {% if current_sorting == 'price_desc' %}selected{% endif %}>Price (high to low)
                                    </option>
                                    <option value="rating_asc"
                                        {% if current_sorting == 'rating_asc' %}selected{% endif %}>Rating (low to high)
                                    </option>
                                    <option value="rating_desc"
                                        {% if current_sorting == 'rating_desc' %}selected{% endif %}>Rating (high to
                                        low)</option>
                                    <option value="name_asc" {% if current_sorting == 'name_asc' %}selected{% endif %}>
                                        Name (A-Z)</option>
                                    <option value="name_desc"
                                        {% if current_sorting == 'name_desc' %}selected{% endif %}>Name (Z-A)</option>
                                    <option value="category_asc"
                                        {% if current_sorting == 'category_asc' %}selected{% endif %}>Category (A-Z)
                                    </option>
                                    <option value="category_desc"
                                        {% if current_sorting == 'category_desc' %}selected{% endif %}>Category (Z-A)
                                    </option>
                                </select>
                            </div>
                        </div>

                        <!-- product count -->
                        <!-- sort select is on top on mobile, and first for medium + screens  -->
                        <div class="col-12 col-md-6 order-md-first">
                            <p class="text-muted mt-3 text-center text-md-left">
                                {% if search_term or current_categories or current_sorting != 'None_None' %}
                                <span class="small"><a href="{% url 'products' %}">Products Home</a> | </span>
                                {% endif %}
                                {{ products|length }} Products{% if search_term %} found for
                                <strong>"{{ search_term }}"</strong>{% endif %}
                            </p>
                        </div>
                    </div>
                </div>

Sort categories by name instead of id - all_products view

        if sortkey == 'category':
            sortkey = 'category__name'

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 3 - sort filter box and back to top button</summary>

Add jquery to products.html for sort button

        
        {% block postloadjs %}
        {{ block.super }}
        <!-- block.super appends the block, instead of replacing it  -->

        <script type="text/javascript">
            // this jquery code is for the sort button 
            // capture change event from sort selector 
            $('#sort-selector').change(function () {
                var selector = $(this);
                var currentUrl = new URL(window.location);

                // the value here refers to the value attribute from the selected option element in the selector box 
                var selectedVal = selector.val();
                if (selectedVal != "reset") {
                    // split the value and sort the first value 
                    var sort = selectedVal.split("_")[0];
                    // specify the direction based on the second item
                    var direction = selectedVal.split("_")[1];

                    // replace the get parFameters in the URL using the search params.set method from the URL object
                    currentUrl.searchParams.set("sort", sort);
                    currentUrl.searchParams.set("direction", direction);

                    // With the new URL now constructed, replace the current location using window.location.replace 
                    // with the updated current URL. Replacing the location will also cause the page to reload which 
                    // will resort the products accordingly.
                    window.location.replace(currentUrl);
                    // if user has selected reset 
                } else {
                    // delete the sort and direction get parameters and then replace the location.
                    currentUrl.searchParams.delete("sort");
                    currentUrl.searchParams.delete("direction");

                    window.location.replace(currentUrl);
                }
            })
        </script>
        {% endblock %}


Add back to top button to end of page 

        <div class="btt-button shadow-sm rounded-0 border border-black">
            <a class="btt-link d-flex h-100">
                <i class="fas fa-arrow-up text-black mx-auto my-auto"></i>
            </a>	
        </div>

Add the js to make the button work 

        <script type="text/javascript">
            $('.btt-link').click(function(e) {
                window.scrollTo(0,0)
            })
        </script>

Add css for the button

        .btt-button {
            height: 42px;
            width: 42px;
            position: fixed;
            bottom: 10px;
            right: 10px;
        }

        .btt-link {
            cursor: pointer;
        }

[Back to top](#walkthrough-steps)
</details>

<hr>

## Shopping bag

[ci video](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/9c06563251a34ed19f5d4273ab4d55ab/?child=first)

<details>
<summary>Create the bag for customers to put things into </summary>

CREATE THE BAG 

- Create the app 'bag'

        python3 manage.py startapp bag

- Add it to installed app in settings

- Start with the simplest view which will render the shopping bag page that as of right now doesn't exist.

        from django.shortcuts import render

        # Create your views here.

        def view_bag(request):
            """ A view that renders the bag contents page """

            return render(request, 'bag/bag.html')

- Create bag.html inside a bag folder inside a templates folder inside the bag folder
    - Copy the structure from the home page but remove content

- create urls.py

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.view_bag, name='view_bag')
        ]

- Include bag urls in main urls.py file

        path('bag/', include('bag.urls')),

- base.html
    - add link to view bag 
    
            {% url 'view_bag'%}

- Add it to the mobile -top-nav too
- start server and check links work in your preview

- Add content to bag.html

            <div class="overlay"></div>
            <div class="container mb-2">
                <div class="row">
                    <div class="col">
                        <hr>
                        <h2 class="logo-font mb-4">Shopping Bag</h2>
                        <hr>
                    </div>
                </div>

                <div class="row">
                    <div class="col">
                        {% if bag_items %}
                            <div class="table-responsive rounded"></div>
                        {% else %}
                            <p class="lead mb-5">Your bag is empty.</p>
                            <a href="{% url 'products' %}" class="btn btn-outline-black rounded-0 btn-lg">
                                <span class="icon">
                                    <i class="fas fa-chevron-left"></i>
                                </span>
                                <span class="text-uppercase">Keep Shopping</span>
                            </a>
                        {% endif %}
                    </div>
                </div>
            </div>


ADD FUNCTIONALITY TO TRACK BAG CONTENTS

- create contexts.py inside bag app

- Add contexts.py to main settings.py under context_processor

            'bag.contexts.bag_contents',

- Add delivery cost variables to bottom of settings.py

        FREE_DELIVERY_THRESHOLD = 50
        STANDARD_DELIVERY_PERCENTAGE = 10

- Add content to contexts.py

        from decimal import Decimal
        from django.conf import settings

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

[Back to top](#walkthrough-steps)
</details>

<hr>

## Adding products to bag

[ci videos](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+EA101+2021_T1/courseware/eb05f06e62c64ac89823cc956fcd8191/f324de58c90e47bd9497bf5839cf1859/?child=first)

<details>
<summary>PART 1 - creating add to bag functionality</summary>

- product_detail.html

    - Add form to add item to bag under the product description

            <form class="form" action=" " method="POST">
                {% csrf_token %}
                <div class="form-row">
                    <div class="col-12">
                        <p class="mt-3"><strong>Quantity:</strong></p>
                        <div class="form-group w-50">
                            <div class="input-group">
                                <input class="form-control qty_input" type="number" name="quantity" value="1" min="1" max="99" data-item_id="{{ product.id }}" id="id_qty_{{ product.id }}">
                            </div>
                        </div>
                    </div>

                    <div class="col-12">
                        <a href="{% url 'products' %}" class="btn btn-outline-black rounded-0 mt-5">
                            <span class="icon">
                                <i class="fas fa-chevron-left"></i>
                            </span>
                            <span class="text-uppercase">Keep Shopping</span>
                        </a>
                        <input type="submit" class="btn btn-black rounded-0 text-uppercase mt-5" value="Add to Bag">
                    </div>
                    <input type="hidden" name="redirect_url" value="{{ request.path }}">
                </div>
            </form>

- Add css for btn-outline-black

        .btn-outline-black {
            background: white;
            color: black !important; /* use important to override link colors for <a> elements */
            border: 1px solid black;
        }

- write the view to handle the above form (bag/views.py)

        def add_to_bag(request, item_id):
            """ Add a quantity of the specified product to the shopping bag """

            quantity = int(request.POST.get('quantity'))
            redirect_url = request.POST.get('redirect_url')
            bag = request.session.get('bag', {})

            if item_id in list(bag.keys()):
                bag[item_id] += quantity
            else:
                bag[item_id] = quantity

            request.session['bag'] = bag
            print(request.session['bag'])
            return redirect(redirect_url)


- Create url for add_to_bag view (bag/urls.py)

        path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),

- Add url to action in form (product_detail.html)

        {% url 'add_to_bag' product.id %}

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 2 - update context processor to make bag contents available across the site</summary>

**INTRO:** In the previous video, we set up the add to bag view in the bag app which ultimately resulted in the creation of a session variable called bag which contains all the items the user would like to purchase.
Because it's a session variable we can access it anywhere we can access the request object like in our views or the custom context processor we made.
In this video, we'll access the shopping bag stored in the session within the context processor in order to add all the bags current items to the context of all templates.
We'll use this functionality to display the total cost of the current shopping bag in the navbar and also start rendering items in the shopping bag template.

<hr>

- Remove print statement from the end of the 'add to bag' view
- Update contexts.py

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
            for item_id, quantity in bag.items():
                # Get the product
                product = get_object_or_404(Product, pk=item_id)
                # Add its quantity times the price to the total
                total += quantity * product.price
                # Increment the product count by the quantity
                product_count += quantity
                # add a dictionary to the list of bag items containing the id, quantity and the product object itself.
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                })

- go to bag.html template
    - render the bag items to ensure it's working

                 {% if bag_items %}
                    <div class="table-responsive rounded">
                        {{ bag_items }}
                    </div>
                {% else %}

    - start server and in preview add products to bag. The total in navbar should update and you should see basket information displayed in bag view
    - [here is the video reviewing this](https://youtu.be/E7dDIN-tElQ?t=238)

- Let's add content to shopping bag table (bag html)
    - It's going to have five columns containing the product image, some info about it, the per-item price the quantity, and the subtotal for that item, and each row will be a new item.

                      <table class="table table-sm table-borderless">
                            <thead class="text-black">
                                <tr>
                                    <th scope="col">Product Info</th>
                                    <th scope="col"></th>
                                    <th scope="col">Price</th>
                                    <th scope="col">Qty</th>
                                    <th scope="col">Subtotal</th>
                                </tr>
                            </thead>

                            {% for item in bag_items %}
                                <tr>
                                    <td class="p-3 w-25">
                                        <img class="img-fluid rounded" src="{{ item.product.image.url }}">
                                    </td>
                                    <td class="py-3">
                                        <p class="my-0"><strong>{{ item.product.name }}</strong></p>
                                        <p class="my-0 small text-muted">SKU: {{ item.product.sku|upper }}</p>
                                    </td>
                                    <td class="py-3">
                                        <p class="my-0">${{ item.product.price }}</p>
                                    </td>
                                    <td class="py-3 w-25">
                                        <p class="my-0">{{ item.quantity }}</p>
                                    </td>
                                    <td class="py-3">
                                        <p class="my-0">${{ item.product.price }}</p>
                                    </td>
                                </tr>
                            {% endfor %}
                            <tr>
                                <td colspan="5" class="pt-5 text-right">
                                    <h6><strong>Bag Total: ${{ total|floatformat:2 }}</strong></h6>
                                    <h6>Delivery: ${{ delivery|floatformat:2 }}</h6>
                                    <h4 class="mt-4"><strong>Grand Total: ${{ grand_total|floatformat:2 }}</strong></h4>
                                    {% if free_delivery_delta > 0 %}
                                        <p class="mb-1 text-danger">
                                            You could get free delivery by spending just <strong>${{ free_delivery_delta }}</strong> more!
                                        </p>
                                    {% endif %}
                                </td>
                            </tr>
                            <tr>
                                <td colspan="5" class="text-right">
                                    <a href="{% url 'products' %}" class="btn btn-outline-black rounded-0 btn-lg">
                                        <span class="icon">
                                            <i class="fas fa-chevron-left"></i>
                                        </span>
                                        <span class="text-uppercase">Keep Shopping</span>
                                    </a>
                                    <a href="" class="btn btn-black rounded-0 btn-lg">
                                        <span class="text-uppercase">Secure Checkout</span>
                                        <span class="icon">
                                            <i class="fas fa-lock"></i>
                                        </span>
                                    </a>
                                </td>
                            </tr>
                        </table>

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 3 - sizes and more fine tuning</summary>

<br>

- Alter the products model so that has sizes is false as default

           has_sizes = models.BooleanField(default=False, null=True, blank=True)

    - This is fine for this project but in real world we'd need inventory of each size etc

    - Make your migrations

            python3 manage.py makemigrations --dry-run
            python3 manage.py makemigrations 
            python3 manage.py migrate --plan
            python3 manage.py migrate

- Open up a shell in your terminal to add sizes to clothes in database

            python3 manage.py shell


            from products.models import Product

        separate out the kitchen, bath etc
            kdbb = ['kitchen_dining', 'bed_bath']

        Call the rest clothes - not 100% accurate since this includes newly added
            clothes = Product.objects.exclude(category__name__in=kdbb)
            clothes.count()
                    out: 128

            for item in clothes:
                item.has_sizes = True
                item.save()

            Product.objects.filter(has_sizes=True)
            Product.objects.filter(has_sizes=True).count()
                    out: 128

            exit()

* Add size selector to product detail template

        {% with product.has_sizes as s %}
            {% if s %}
                <div class="col-12">
                    <p><strong>Size:</strong></p>
                    <select class="form-control rounded-0 w-50" name="product_size" id='id_product_size'>
                        <option value="xs">XS</option>
                        <option value="s">S</option>
                        <!-- M is the default  -->
                        <option value="m" selected>M</option>
                        <option value="l">L</option>
                        <option value="xl">XL</option>
                    </select>
                </div>
            {% endif %}
        
- Add size to product info on shopping bag page in here

        <!-- product name, size and sku  -->
        <td class="py-3">
            <p class="my-0"><strong>{{ item.product.name }}</strong></p>
            <p class="my-0"><strong>Size: </strong>{% if item.product.has_sizes %}{{ item.size|upper }}{% else %}N/A{% endif %}</p>
            <p class="my-0 small text-muted">SKU: {{ item.product.sku|upper }}</p>
        </td>


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 4 - tidy up wrong categories with sizes and add code to handle product sizes</summary>

[ci youtube video](https://youtu.be/bQuggmgIEEs?t=7)

**FIX ITEMS WITH SIZES THAT SHOULDN'T HAVE THEM**

- Runserver and go through all specials and find the items that shouldn't have sizes
- Go to each one in the admin panel and change has_sizes to no

<br>

**LET'S GIVE THE SHOPPING BAG SOME SIZE INFO**

- First let's deal with the add_to_bag view

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

- Now let's handle the context.py

    - Go to bagcontents

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

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 5 - Add increment/decrement buttons</summary>

**Update the quantity selector**

- Go to product_detail page

                        <div class="col-12">
                            <p class="mt-3"><strong>Quantity:</strong></p>
                            <div class="form-group w-50">
                                <div class="input-group">

                                    <div class="input-group-prepend">
                                        <!-- These IDs are for the javascript  -->
                                        <button class="decrement-qty btn btn-black rounded-0" 
                                            data-item_id="{{ product.id }}" id="decrement-qty_{{ product.id }}">
                                            <span class="icon">
                                                <i class="fas fa-minus"></i>
                                            </span>
                                        </button>
                                    </div>
                                    <input class="form-control qty_input" type="number"
                                        name="quantity" value="1" min="1" max="99"
                                        data-item_id="{{ product.id }}"
                                        id="id_qty_{{ product.id }}">

                                    <div class="input-group-append">
                                        <button class="increment-qty btn btn-black rounded-0"
                                            data-item_id="{{ product.id }}" id="increment-qty_{{ product.id }}">
                                            <span class="icon">
                                                <i class="fas fa-plus"></i>
                                            </span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

- write the javascript (as an include, as it will be reused in the shoppong bag page) to make the buttons work

    - products/templates/includes/quantity_input_script.html

                <script type="text/javascript">

                // Disable +/- buttons outside 1-99 range
                function handleEnableDisable(itemId) {
                    // get current quantity value based on itemId 
                    // the id is the id attribute on the input box in product detail page 
                    var currentValue = parseInt($(`#id_qty_${itemId}`).val());
                    var minusDisabled = currentValue < 2;
                    var plusDisabled = currentValue > 98;
                    // prop sets disabled setting to true/false 
                    $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
                    $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
                }

                // Ensure proper enabling/disabling of all inputs on page load
                var allQtyInputs = $('.qty_input');
                for(var i = 0; i < allQtyInputs.length; i++){
                    var itemId = $(allQtyInputs[i]).data('item_id');
                    handleEnableDisable(itemId);
                }

                // Check enable/disable every time the input is changed
                $('.qty_input').change(function() {
                    var itemId = $(this).data('item_id');
                    handleEnableDisable(itemId);
                });

                // Increment quantity
                $('.increment-qty').click(function(e) {
                    // prevent default action of button 
                e.preventDefault();
                    // closest goes up the dom, find goes down 
                    // So from the clicked button go up to the first input group class, 
                    // then go down to find the first quantity input
                var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
                // Cache that value
                var currentValue = parseInt($(closestInput).val());
                //  set the input boxes new value to the current value plus one.
                $(closestInput).val(currentValue + 1);
                //    call function to disable/enable buttons each time a button is clicked 
                var itemId = $(this).data('item_id');
                handleEnableDisable(itemId);
                });

                // Decrement quantity
                // Same as above but -1 instead of + 
                $('.decrement-qty').click(function(e) {
                e.preventDefault();
                var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
                var currentValue = parseInt($(closestInput).val());
                $(closestInput).val(currentValue - 1);
                var itemId = $(this).data('item_id');
                handleEnableDisable(itemId);
                });
            </script>



[Back to top](#walkthrough-steps)
</details>

<details>
<summary>PART 6 - add quantity selector to shopping bag pages </summary>

[youtube video](https://youtu.be/0rRNZa7BR_Y)

* Replace quantity on bag.html with form with POST method

        <form class="form update-form" method="POST" action="">
                                            {% csrf_token %}
                                            <div class="form-group">
                                                <div class="input-group">
                                                    <div class="input-group-prepend">
                                                        <button class="decrement-qty btn btn-sm btn-black rounded-0" 
                                                            data-item_id="{{ item.item_id }}" id="decrement-qty_{{ item.item_id }}">
                                                            <span>
                                                                <i class="fas fa-minus fa-sm"></i>
                                                            </span>
                                                        </button>
                                                    </div>
                                                    <input class="form-control form-control-sm qty_input" type="number"
                                                        name="quantity" value="{{ item.quantity }}" min="1" max="99"
                                                        data-item_id="{{ item.item_id }}"
                                                        id="id_qty_{{ item.item_id }}">
                                                    <div class="input-group-append">
                                                        <button class="increment-qty btn btn-sm btn-black rounded-0"
                                                            data-item_id="{{ item.item_id }}" id="increment-qty_{{ item.item_id }}">
                                                            <span>
                                                                <i class="fas fa-plus fa-sm"></i>
                                                            </span>
                                                        </button>
                                                    </div>
                                                    {% if item.product.has_sizes %}
                                                        <input type="hidden" name="product_size" value="{{ item.size }}">
                                                    {% endif %}
                                                </div>
                                            </div>
                                        </form>

- Check it's working on the server
    - Quantity isn't showing on items with sizes - issue with context. 
    - In bag contents, for the code where size is supplied change this:

                    'quantity': item_data,

    - To this     

                    'quantity': quantity,

- Now let's make the increment buttons on the bag page work by copying the end of the product_detail page

            {% block postloadjs %}
            {{ block.super }}
            {% include 'products/includes/quantity_input_script.html' %}
            {% endblock %}

- There's currently no way to submit the form. Handle that with JS
    - Add these under the form to update/remove items

                <a class="update-link text-info"><small>Update</small></a>
                <a class="remove-item text-danger float-right" id="remove_{{ item.item_id }}" data-size="{{ item.size }}"><small>Remove</small></a>

    - Write the JS to handle these two being clicked at the bottom of bag.html
                
                <script type="text/javascript">
                    // Update quantity on click
                    // use the previous method to find the most recently seen update form in the 
                    // Dom. Store the form in a variable and then call the forms submit method.
                    $('.update-link').click(function(e) {
                        var form = $(this).prev('.update-form');
                        form.submit();
                    })

                    // Remove item and reload on click
                    $('.remove-item').click(function(e) {
                        var csrfToken = "{{ csrf_token }}";
                        // get itemid
                        var itemId = $(this).attr('id').split('remove_')[1];
                        // get size 
                        var size = $(this).data('size');
                        // Get url of item
                        var url = `/bag/remove/${itemId}`;
                        // the object we'll use to send this data to the server
                        var data = {'csrfmiddlewaretoken': csrfToken, 'size': size};

                        $.post(url, data)
                        .done(function() {
                            location.reload();
                        });
                    })
                </script>

- add update and delete classes to back to top link in css
[Back to top](#walkthrough-steps)
</details>

<hr>

## Adjusting quantity of items in bag

<details>

<summary>Open me here</summary>

<details>
<summary>Part 1 - Adjusting bag quantity </summary>

Create view in bag/views.py for adjusting bag       

        def adjust_bag(request, item_id):
            """Adjust the quantity of the specified product to the specified amount"""

            quantity = int(request.POST.get('quantity'))
            size = None
            if 'product_size' in request.POST:
                size = request.POST['product_size']
            bag = request.session.get('bag', {})

            if size:
                if quantity > 0:
                    bag[item_id]['items_by_size'][size] = quantity
                else:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
            else:
                if quantity > 0:
                    bag[item_id] = quantity
                else:
                    bag.pop(item_id)

            request.session['bag'] = bag
            return redirect(reverse('view_bag'))

        
        Import reverse at the top

And for removing items from the bag 

        def remove_from_bag(request, item_id):
            """Remove the item from the shopping bag"""

            try:
                size = None
                if 'product_size' in request.POST:
                    size = request.POST['product_size']
                bag = request.session.get('bag', {})

                if size:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
                else:
                    bag.pop(item_id)

                request.session['bag'] = bag
                return HttpResponse(status=200)

            except Exception as e:
                return HttpResponse(status=500)


        Import httpresponse at the top

Create URLS for them in bag/urls.py

        
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'),


Give template proper action url (bag.html)

    * for adjust 

            <form class="form update-form" method="POST" action="{% url 'adjust_bag' item.item_id %}">

</details>

<details>
<summary>Part 2 - Fixing remove function and creating filter to calculate subtotal </summary>

Update javascript and template html for remove link to match the view

    * Change 'size' to 'product_size' in bag.html 

Replace the slim version of bootstrap with the full

        <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

    This has more ajax functions such as post

The remove function should now work

**Note** The subtotal on the bag page doesn't update for products. Let's fix this.

* Create bagtools.py in new templatetags folder

        from django import template

        register = template.Library()

        @register.filter(name='calc_subtotal')
        def calc_subtotal(price, quantity):
            return price * quantity

* Create empty __init__.py file so the directory is treated as a python package and makes it available for imports and to use in templates

* Load the template into the top of bag.html

        {% load bag_tools %}

Then add it into the price template after a pipe

</details>

[Back to top](#walkthrough-steps)


</details>

<hr>

## Toasts

<details>
<summary>Open me</summary>

<details>
<summary>Part 1</summary>

[ci video](https://youtu.be/cwhROnUBZbQ)

Create a toast folder inside includes

    * Create toast_error, toast_info, toast_success, toast_warning files from Bootstrap

Add to the messages section of base.html

        {% if messages %}
            <div class="message-container">
                {% for message in messages %}
                    {% with message.level as level %}
                        {% if level == 40 %}
                            {% include 'includes/toasts/toast_error.html' %}
                        {% elif level == 30 %}
                            {% include 'includes/toasts/toast_warning.html' %}
                        {% elif level == 25 %}
                            {% include 'includes/toasts/toast_success.html' %}
                        {% else %}
                            {% include 'includes/toasts/toast_info.html' %}
                        {% endif %}
                {% endwith %}
                {% endfor %}
            </div>
        {% endif %}


Go to bag views.py

* Do some imports 

        from django.contrib import messages
        from products.models import Product

*  Add success message to add to bag view

         messages.success(request, f'Added {product.name} to your bag')

Add to postloadjs of base.html

        <script type="text/javascript">
            $('.toast').toast('show');
        </script>

Go to settings.py

        MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 2</summary>

[ci video](https://youtu.be/DbTOSYWMego)

Add css to position toast messages

        /* ------------------------------- bootstrap toasts */

        .message-container {
            position: fixed;
            top: 72px;
            right: 15px;
            z-index: 99999999999;
        }

        .custom-toast {
            overflow: visible;
        }

        .toast-capper {
            height: 2px;
        }


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 3</summary>

[ci video](https://youtu.be/fm4Xrv_TpdE)

Add more messages to bag views.py - add to bag, adjust bag, remove from bag

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 4</summary>

[ci video](https://youtu.be/5GanYa6YCbQ)

Add css for arrows under toasts

Add to your success toast html file to show preview of bag contents

        <div class="toast custom-toast rounded-0 border-top-0" data-autohide="false">
            <div class="arrow-up arrow-success"></div>
            <div class="w-100 toast-capper bg-success"></div>
            <div class="toast-header bg-white text-dark">
                <strong class="mr-auto">Success!</strong>
                <button type="button" class="ml-2 mb-1 close text-dark" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body bg-white">
                <div class="row">
                    <div class="col">
                        {{ message }}
                        <hr class="mt-1 mb-3">
                    </div>
                </div>
                {% if grand_total %}
                    <p class="logo-font bg-white text-black py-1">Your Bag ({{ product_count }})</p>
                    <div class="bag-notification-wrapper">
                        {% for item in bag_items %}
                            <div class="row">
                                <div class="col-3 my-1">
                                    <img class="w-100" src="{{ item.product.image.url }}">
                                </div>
                                <div class="col-9">
                                    <p class="my-0"><strong>{{ item.product.name }}</strong></p>
                                    <p class="my-0 small">Size: {% if item.product.has_sizes %}{{ item.size|upper }}{% else %}N/A{% endif %}</p>
                                    <p class="my-0 small text-muted">Qty: {{ item.quantity }}</p>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                    <div class="row">
                        <div class="col">
                            <strong><p class="mt-3 mb-1 text-black">
                                Total{% if free_delivery_delta > 0 %} (Exc. delivery){% endif %}: 
                                <span class="float-right">${{ total|floatformat:2 }}</span>
                            </p></strong>
                            {% if free_delivery_delta > 0 %}
                                <p class="mb-0 p-2 bg-warning shadow-sm text-black text-center">
                                    Spend <strong>${{ free_delivery_delta }}</strong> more to get free next day delivery!
                                </p>
                            {% endif %}
                            <a href="{% url 'view_bag' %}" class="btn btn-black btn-block rounded-0">
                                <span class="text-uppercase">Go To Secure Checkout</span>
                                <span class="icon">
                                    <i class="fas fa-lock"></i>
                                </span>
                            </a>
                        </div>
                    </div>
                {% endif %}
            </div>
        </div>

Add css for bag notification wrapper

            .bag-notification-wrapper {
            height: 100px;
            overflow-x: hidden;
            overflow-y: auto;
            }


Discusses a vulnerability gitpod points out when pushes are made - I didn't get that though

</details>

[Back to top](#walkthrough-steps)
</details>

<hr>

## CHECKOUT APP

<details>
<summary>Models pt 1</summary>

[ci video](https://youtu.be/n0MS3fHBwEU)

Create new app for checkout

        python3 manage.py startapp checkout

* Add it to settings.py

Create models for checkout

        import uuid
        # uuid needed to generate order number

        from django.db import models
        from django.db.models import Sum
        from django.conf import settings

        from products.models import Product

        # model for each model 
        class Order(models.Model):
            # order no. is auto generated and unique 
            order_number = models.CharField(max_length=32, null=False, editable=False)
            full_name = models.CharField(max_length=50, null=False, blank=False)
            email = models.EmailField(max_length=254, null=False, blank=False)
            phone_number = models.CharField(max_length=20, null=False, blank=False)
            country = models.CharField(max_length=40, null=False, blank=False)
            postcode = models.CharField(max_length=20, null=True, blank=True)
            town_or_city = models.CharField(max_length=40, null=False, blank=False)
            street_address1 = models.CharField(max_length=80, null=False, blank=False)
            street_address2 = models.CharField(max_length=80, null=True, blank=True)
            county = models.CharField(max_length=80, null=True, blank=True)
            date = models.DateTimeField(auto_now_add=True)
            delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
            order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
            grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)


        # A line item is basically an individual shopping bag item 
        class OrderLineItem(models.Model):
            # For each item in an order, this info is created and added to the order. Then the delivery cost, order total and grand totals are updated
            order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
            product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
            product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
            quantity = models.IntegerField(null=False, blank=False, default=0)
            lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Models pt 2</summary>

[ci video](https://youtu.be/l1Z9Aau0V08)

Create model methods in checkout/models.py

* For order model

        # prepending the method name with an underscore means it will only be used inside this class 
        def _generate_order_number(self):
            """
            Generate a random, unique order number using UUID
            This generated a string of 32 numbers
            """
            return uuid.uuid4().hex.upper()

        def update_total(self):
            """
            Update grand total each time a line item is added,
            accounting for delivery costs using aggregate function.
            """
            # This works is by using the sum function across all the line-item 
            # total fields for all line items on this order. The default behaviour
            # is to add a new field to the query set called line-item total sum.
            # Which we can then get and set the order total to that.
            self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
            # Now we can calculate delivery costs
            if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
                self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            else:
                self.delivery_cost = 0
            # Now calculate grand total
            self.grand_total = self.order_total + self.delivery_cost
            self.save()

        # override default save method 
        def save(self, *args, **kwargs):
            """
            Override the original save method to set the order number
            if it hasn't been set already.
            """
            if not self.order_number:
                # If the current order doesn't have an order number, one is assigned
                self.order_number = self._generate_order_number()
            # then execute original save method
            super().save(*args, **kwargs)

        def __str__(self):
            return self.order_number

* For lineitem model

        def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

        def __str__(self):
            return f'SKU {self.product.sku} on order {self.order.order_number}'

Run dry migrations

        python3 manage.py makemigrations --dry-run

Run migrations

        python3 manage.py makemigrations 

Plan execution

        python3 manage.py migrate --plan

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Admin, signals and forms pt 1</summary>

[ci video](https://youtu.be/gm0BQEyJP_o)

* Add checkout models to checkout admin.py

        from django.contrib import admin
        from .models import Order, OrderLineItem


        class OrderLineItemAdminInline(admin.TabularInline):
            # Allows us to add and edit line items in admin in the order model
            model = OrderLineItem
            readonly_fields = ('lineitem_total',)


        class OrderAdmin(admin.ModelAdmin):
            # add inline to this panel
            inlines = (OrderLineItemAdminInline,)

            # Things that are calculated by our order model that can't be edited
            readonly_fields = ('order_number', 'date',
                            'delivery_cost', 'order_total',
                            'grand_total',)

            # this isn't fully necessary but allows us to specify order the fields in admin panel
            fields = ('order_number', 'date', 'full_name',
                    'email', 'phone_number', 'country',
                    'postcode', 'town_or_city', 'street_address1',
                    'street_address2', 'county', 'delivery_cost',
                    'order_total', 'grand_total',)

            # Which columns are displayed in the order list 
            list_display = ('order_number', 'date', 'full_name',
                            'order_total', 'delivery_cost',
                            'grand_total',)

            ordering = ('-date',)

        admin.site.register(Order, OrderAdmin)

* Check the admin panel

        python3 manage.py runserver

* Call methods which update totals and delivery cost of order using signals

        * create signals.py in checkout 

                # post here means after 
                from django.db.models.signals import post_save, post_delete
                from django.dispatch import receiver

                from .models import OrderLineItem

                @receiver(post_save, sender=OrderLineItem)
                def update_on_save(sender, instance, created, **kwargs):
                    """
                    Update order total on lineitem update/create
                    Handles signals from the post save event
                    Here: sender=orderlineitem, instance of the model that sent it, a boolean
                    by django saying if this is a new instance or one being updated and any 
                    keyword arguements
                    Our code inside the method is really simple.
                    We just have to access instance.order - which refers to the order this 
                    specific line item is related to - and call the update_total method on it.
                    To execute this function anytime the post_save signal is sent use the 
                    receiver decorator, telling it we're receiving post saved signals from the
                    OrderLineItem model.
                    """
                    instance.order.update_total()

                @receiver(post_delete, sender=OrderLineItem)
                def update_on_save(sender, instance, **kwargs):
                    """
                    Update order total on lineitem delete
                    Same same as above, but different
                    * Note: There's an error here that will be addressed later *
                    """
                    instance.order.update_total()

* Let django know there's a new signals module with listeners

    * checkout apps.py

            class CheckoutConfig(AppConfig):
            name = 'checkout'

            def ready(self):
                import checkout.signals

    With that done, every time a line item is saved or deleted.
    Our custom update total model method will be called.
    Updating the order totals automatically.

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Admin, signals and forms pt 2</summary>

[ci video](https://youtu.be/0cGRqIHvSf8)

* Create checkout form

    * forms.py in checkout

            from django import forms
            from .models import Order


            class OrderForm(forms.ModelForm):
                class Meta:
                    model = Order
                    fields = ('full_name', 'email', 'phone_number',
                            'street_address1', 'street_address2',
                            'town_or_city', 'postcode', 'country',
                            'county',)

                def __init__(self, *args, **kwargs):
                    """
                    Add placeholders and classes, remove auto-generated
                    labels and set autofocus on first field
                    """
                    # call default method to set up form as it would be by default
                    super().__init__(*args, **kwargs)
                    # Add placeholders to boxes
                    placeholders = {
                        'full_name': 'Full Name',
                        'email': 'Email Address',
                        'phone_number': 'Phone Number',
                        'country': 'Country',
                        'postcode': 'Postal Code',
                        'town_or_city': 'Town or City',
                        'street_address1': 'Street Address 1',
                        'street_address2': 'Street Address 2',
                        'county': 'County',
                    }

                    # Set cursor to start in full name when page loads 
                    self.fields['full_name'].widget.attrs['autofocus'] = True
                    # Go through the list
                    for field in self.fields:
                        # If the field is required, add a star 
                        if self.fields[field].required:
                            placeholder = f'{placeholders[field]} *'
                        else:
                            placeholder = placeholders[field]
                        # set placeholder values as per above
                        self.fields[field].widget.attrs['placeholder'] = placeholder
                        # Add the css class we haven't created yet
                        self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                        # Remove labels
                        self.fields[field].label = False

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Templates and views pt 1</summary>

[ci video](https://youtu.be/eAja_pKhiCM)

* Create checkout view

        * views.py 

                from django.shortcuts import render, redirect, reverse
                from django.contrib import messages

                from .forms import OrderForm


                def checkout(request):
                    bag = request.session.get('bag', {})
                    # if bag is empty
                    if not bag:
                        messages.error(request, "There's nothing in your bag at the moment")
                        # redirect back to the checkout page 
                        return redirect(reverse('products'))

                    # create empty instance of order form 
                    order_form = OrderForm()
                    template = 'checkout/checkout.html'
                    context = {
                        'order_form': order_form,
                    }

                    return render(request, template, context)

* Create urls.py in checkout 

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.checkout, name='checkout')
        ]

* Add this to project urls.py

        path('checkout/', include('checkout.urls')),

* Create templates folder in checkout

    * Create checkout folder in there
    
    * Create checkout.html template

    * Install crispy forms 

            pip3 install django-crispy-forms

    * Add it to settings.py installed apps

            # other
            'crispy_forms',

        And tell it which version to use

            CRISPY_TEMPLATE_PACK = 'bootstrap4'

    * Make crispy available across your app

            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]

* Add crispy to your requirements

        pip3 freeze > requirements.txt



[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Templates and views pt 2</summary>

[ci video](https://youtu.be/NKPBP-YQmhk)

Create form in checkout.html

        <!-- ORDER FORM  -->
            <div class="col-12 col-lg-6">
                <p class="text-muted">Please fill out the form below to complete your order</p>
                <form action="{% url 'checkout' %}" method="POST" id="payment-form">
                    {% csrf_token %}

                    <!-- DETAILS FIELDSET  -->
                    <fieldset class="rounded px-3 mb-5">
                        <legend class="fieldset-label small text-black px-2 w-auto">Details</legend>
                        {{ order_form.full_name | as_crispy_field }}
                        {{ order_form.email | as_crispy_field }}
                    </fieldset>

                    <!-- DELIVERY FIELDSET  -->
                    <fieldset class="rounded px-3 mb-5">
                        <legend class="fieldset-label small text-black px-2 w-auto">Delivery</legend>
                        {{ order_form.phone_number | as_crispy_field }}
                        {{ order_form.country | as_crispy_field }}
                        {{ order_form.postcode | as_crispy_field }}
                        {{ order_form.town_or_city | as_crispy_field }}
                        {{ order_form.street_address1 | as_crispy_field }}
                        {{ order_form.street_address2 | as_crispy_field }}
                        {{ order_form.county | as_crispy_field }}
                        <div class="form-check form-check-inline float-right mr-0">
                            <!-- checkbox to ask users if they want info saved to their profile  -->
                            <!-- If checked it saves info to their profile and autofills form next time they checkout  -->
							{% if user.is_authenticated %}
								<label class="form-check-label" for="id-save-info">Save this delivery information to my profile</label>
                                <input class="form-check-input ml-2 mr-0" type="checkbox" id="id-save-info" name="save-info" checked>
							<!-- links for them to signup/login to save info -->
                            {% else %}
								<label class="form-check-label" for="id-save-info">
                                    <a class="text-info" href="{% url 'account_signup' %}">Create an account</a> or 
                                    <a class="text-info" href="{% url 'account_login' %}">login</a> to save this information
                                </label>
							{% endif %}
						</div>
                    </fieldset>

                    <!-- PAYMENT FIELDSET  -->
                    <fieldset class="px-3">
                        <legend class="fieldset-label small text-black px-2 w-auto">Payment</legend>
                        <!-- A Stripe card element will go here -->
                        <div class="mb-3" id="card-element"></div>

                        <!-- Used to display form errors -->
                        <div class="mb-3 text-danger" id="card-errors" role="alert"></div>
                    </fieldset>

                    <!-- Link to shopping bag -->
                    <div class="submit-button text-right mt-5 mb-2">                    
						<a href="{% url 'view_bag' %}" class="btn btn-outline-black rounded-0">
							<span class="icon">
								<i class="fas fa-chevron-left"></i>
							</span>
							<span class="font-weight-bold">Adjust Bag</span>
						</a>
                        
                        <!-- submit button  -->
						<button id="submit-button" class="btn btn-black rounded-0">
							<span class="font-weight-bold">Complete Order</span>
							<span class="icon">
								<i class="fas fa-lock"></i>
							</span>
						</button>

                        <!-- charge notification  -->
						<p class="small text-danger my-0">
							<span class="icon">
								<i class="fas fa-exclamation-circle"></i>
							</span>
							<span>Your card will be charged <strong>${{ grand_total|floatformat:2 }}</strong></span>
						</p>
					</div>
                </form>
            </div>


Add product info for bag

        <!-- column before form, but to the right on larger screens  -->
            <div class="col-12 col-lg-6 order-lg-last mb-5">
                <!-- order summary  -->
                <p class="text-muted">Order Summary ({{ product_count }})</p>
                <div class="row">
                    <div class="col-7 offset-2">
                        <p class="mb-1 mt-0 small text-muted">Item</p>
                    </div>
                    <div class="col-3 text-right">
                        <p class="mb-1 mt-0 small text-muted">Subtotal</p>
                    </div>
                </div>
                <!-- Show each item  -->
                {% for item in bag_items %}
                    <div class="row">

                        <!-- Show product image  -->
                        <div class="col-2 mb-1">
                            <a href="{% url 'product_detail' item.product.id %}">
                                {% if item.product.image %}
                                    <img class="w-100" src="{{ item.product.image.url }}" alt="{{ product.name }}">
                                {% else %}
                                    <img class="w-100" src="{{ MEDIA_URL }}noimage.png" alt="{{ product.name }}">
                                {% endif %}
                            </a>
                        </div>

                        <!-- product info  -->
                        <div class="col-7">
                            <p class="my-0"><strong>{{ item.product.name }}</strong></p>
                            <p class="my-0 small">Size: {% if item.product.has_sizes %}{{ item.size|upper }}{% else %}N/A{% endif %}</p>
                            <p class="my-0 small text-muted">Qty: {{ item.quantity }}</p>
                        </div>
                        <!-- subtotal  -->
                        <div class="col-3 text-right">
                            <p class="my-0 small text-muted">${{ item.product.price | calc_subtotal:item.quantity }}</p>
                        </div>
                    </div>
                {% endfor %}

                <hr class="my-0">
                <!-- totals and delivery cost  -->
                <div class="row text-black text-right">
                    <div class="col-7 offset-2">
                        <p class="my-0">Order Total:</p>
                        <p class="my-0">Delivery:</p>
                        <p class="my-0">Grand Total:</p>
                    </div>
                    <div class="col-3">
                        <p class="my-0">${{ total | floatformat:2 }}</p>
                        <p class="my-0">${{ delivery | floatformat:2 }}</p>
                        <p class="my-0"><strong>${{ grand_total | floatformat:2 }}</strong></p>
                    </div>
                </div>
            </div>


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Templates and views pt 3</summary>

[ci video](https://youtu.be/atjWMjFMhp0)

Add media context processor to settings.py

        'django.template.context_processors.media',

Add checkout url to checkout button on bag.html

        <a href="{% url 'checkout' %}" class="btn btn-black rounded-0 btn-lg">

[Back to top](#walkthrough-steps)

</details>

<hr>

## STRIPE PAYMENTS

<details>
<summary>Part 1 - signup to stripe</summary>

[ci video](https://youtu.be/or9zOswvISY)

Add css to checkout.css

        .fieldset-label {
            position: relative;
            right: .5rem;
        }

        #payment-form .form-control,
        #card-element {
            color: #000;
            border: 1px solid #000;
        }

Add Stripe 

    * Go to stripe.com and sign up/in


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 2 - add stripe js</summary>

[video link](https://youtu.be/eUcMh5s_27I)

[Accepting a payment with stripe](https://stripe.com/docs/payments/accept-a-payment#web-collect-card-details)

* Get the js script link from stripe

        <script src="https://js.stripe.com/v3/"></script>

[link for source](https://stripe.com/docs/js/including#:~:text=no%20code%20required.-,Including%20Stripe.js,-Include%20the%20Stripe)

* Add it to core js of base.html

* Add postload js to bottom of checkout.html

        {% block postloadjs %}
            {{ block.super }}
            {{ stripe_public_key|json_script:"id_stripe_public_key" }}
            {{ client_secret|json_script:"id_client_secret" }}
            <script src="{% static 'checkout/js/stripe_elements.js' %}"></script>
        {% endblock %}

* Get the publishable key from the stripe dashboard

        pk_test_51K1HPjFEToCWPRVclerd629oZ2GPMA7MZ35nvCP1MFMF3TOaGag82Zcnss3Yks7VrpnTs54aTBofqbdW71E4mX19009CY8EerJ

* Go to checkout/views.py
    * Add it to context 

        'stripe_public_key': 'pk_test_51K1HPjFEToCWPRVclerd629oZ2GPMA7MZ35nvCP1MFMF3TOaGag82Zcnss3Yks7VrpnTs54aTBofqbdW71E4mX19009CY8EerJ'

    * Add test value for client secret 

        'client_secret': 'test client secret',

* Go to your checkout preview and make sure these two values are at the bottom if you inspect the page

* Create stripe_elements.js beside checkout/css

    [style](https://stripe.com/docs/js/payment_request/events/on_shipping_option_change#:~:text=94941%27%2C%0A%20%20country%3A%20%27US%27%2C%0A%7D-,The%20Style%20object,-Elements%20are%20styled)


    // get stripe key, removing the quotation mark characters
    var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
    var client_secret = $('#id_client_secret').text().slice(1, -1);
    // create stripe variable 
    var stripe = Stripe(stripe_public_key);
    // Use stripe variable to get stripe elements 
    var elements = stripe.elements();
    // copy style from (https://stripe.com/docs/js/payment_request/events/on_shipping_option_change#:~:text=94941%27%2C%0A%20%20country%3A%20%27US%27%2C%0A%7D-,The%20Style%20object,-Elements%20are%20styled)
    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    // use elements to create card with style from above
    var card = elements.create('card', {style: style});
    // mount the card to the div we made previously 
    card.mount('#card-element');



* Add stripe css from documentation, with our custom stripe-style-input class name from earlier

        .StripeElement,
        .stripe-style-input {
        box-sizing: border-box;
        height: 40px;
        padding: 10px 12px;
        border: 1px solid transparent;
        border-radius: 0px;
        background-color: white;
        box-shadow: 0 1px 3px 0 #e6ebf1;
        -webkit-transition: box-shadow 150ms ease;
        transition: box-shadow 150ms ease;
        }

        .StripeElement--focus,
        .stripe-style-input:focus,
        .stripe-style-input:active {
        box-shadow: 0 1px 3px 0 #cfd7df;
        }

        .StripeElement--webkit-autofill {
        background-color: #fefde5 !important;
        }

        .stripe-style-input::placeholder {
            color: #aab7c4;
        }

[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 3 - install stripe and environment variables </summary>

[ci video](https://youtu.be/MOYj1OGi76k)

Give card element some functionality

* Add error message for card details 

        // Handle realtime validation errors on the card element
        card.addEventListener('change', function (event) {
            // add listener to card element and check for errors everytime it changes 
            var errorDiv = document.getElementById('card-errors');
            if (event.error) {
                // If there are, display them in the card errors div 
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${event.error.message}</span>
                `;
                $(errorDiv).html(html);
            } else {
                // otherwise it will be blank 
                errorDiv.textContent = '';
            }
        });
**Note:** How stripe works [video moment](https://youtu.be/MOYj1OGi76k?t=128)

    1. Checkout view creates stripe payment intent
    2. Stripe returns client_secret, which we return to the template
    3. Use client_secret in the template to call confirmCardPaymeny() and verify the card 

We need to calculate the bag total for this

Checkout/views.py 

* import bag contents function

        from bag.contexts import bag_contents

* Update checkout function on that page

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
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

* Install stripe 

    pip3 install stripe

* Import it to the top of views.py

    import stripe

* Import settings 

    from django.conf import settings

* Go to settings.py

    # Stripe
    FREE_DELIVERY_THRESHOLD = 50
    STANDARD_DELIVERY_PERCENTAGE = 10
    STRIPE_CURRENCY = 'usd'
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

* Set the public and secret keys in gitpod terminal, copying values from stripe dashboard
(There are definitely other ways to set environment variables)

        export STRIPE_PUBLIC_KEY=pk_test_51K1HPjFEToCWPRVclerd629oZ2GPMA7MZ35nvCP1MFMF3TOaGag82Zcnss3Yks7VrpnTs54aTBofqbdW71E4mX19009CY8EerJ

        export STRIPE_SECRET_KEY=copy_key_here

    NOTE: These will have to be exported each time you start workspace unless you save them in gitpod workspace variable

            * Go to gitpod dashboard
            * Settings
            * Variables
            * Enter the values
            * Stop and reopen the workspace


[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 4 - get view to return proper secrets </summary>

[ci video](https://youtu.be/rp_ERUy7nb4)

Create payment intent in views.py

        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

If you print the intent and refresh the checkout page, this is what shows up in the terminal when the item is 411.98 for two items

        {
            "amount": 41198,
            "amount_capturable": 0,
            "amount_received": 0,
            "application": null,
            "application_fee_amount": null,
            "automatic_payment_methods": null,
            "canceled_at": null,
            "cancellation_reason": null,
            "capture_method": "automatic",
            "charges": {
                "data": [],
                "has_more": false,
                "object": "list",
                "total_count": 0,
                "url": "/v1/charges?payment_intent=pi_3K1J1SFEToCWPRVc1QdY1xta"
            },
            "client_secret": "pi_3K1J1SFEToCWPRVc1QdY1xta_secret_g6mQs0Fq7XhhOJRWXwsCmC9yg",
            "confirmation_method": "automatic",
            "created": 1638227554,
            "currency": "usd",
            "customer": null,
            "description": null,
            "id": "pi_3K1J1SFEToCWPRVc1QdY1xta",
            "invoice": null,
            "last_payment_error": null,
            "livemode": false,
            "metadata": {},
            "next_action": null,
            "object": "payment_intent",
            "on_behalf_of": null,
            "payment_method": null,
            "payment_method_options": {
                "card": {
                "installments": null,
                "network": null,
                "request_three_d_secure": "automatic"
                }
            },
            "payment_method_types": [
                "card"
            ],
            "receipt_email": null,
            "review": null,
            "setup_future_usage": null,
            "shipping": null,
            "source": null,
            "statement_descriptor": null,
            "statement_descriptor_suffix": null,
            "status": "requires_payment_method",
            "transfer_data": null,
            "transfer_group": null
            }

* Update your views.py so it looks like this

    <details>
    <summary>Reveal views.py</summary>
    
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
    
    </details>
[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 5 - add listener to payment forms submit event</summary>

[ci video](https://youtu.be/YtVMZItdI0E)

[the modern link](https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements#web-submit-payment)

go to checkout js and add code to handle form submission
            
            // Handle form submit
            var form = document.getElementById('payment-form');

            form.addEventListener('submit', function(ev) {
                ev.preventDefault();
                card.update({ 'disabled': true});
                $('#submit-button').attr('disabled', true);
                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                    }
                }).then(function(result) {
                    if (result.error) {
                        var errorDiv = document.getElementById('card-errors');
                        var html = `
                            <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>`;
                        $(errorDiv).html(html);
                        card.update({ 'disabled': false});
                        $('#submit-button').attr('disabled', false);
                    } else {
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });
            });

You should now be able to successfully test your checkout form (using 4242)

Now go back to stripe dashboard

* developers
* events
    * Your payment should be visible
    
[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 6 - handle Post for form </summary>

[ci video](https://youtu.be/CZnAfbguNys)

[test card numbers](https://stripe.com/docs/testing)

* Update the checkout view to handle the posting for the form 

<details>
<summary>Show here</summary>


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

</details>

* import models at the top of the views page 

            from .models import Order, OrderLineItem
            from products.models import Product


* Create checkout_success view

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

* Import get 404

            from django.shortcuts import render, redirect, reverse, get_object_or_404

* Go to checkout urls.py

            path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),



[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 7 - checkout success template</summary>

[ci video](https://youtu.be/KIyMQI2ZrOE)

* create checkout success html beside checkout.html

            {% extends "base.html" %}
            {% load static %}

            {% block extra_css %}
                <link rel="stylesheet" href="{% static 'checkout/css/checkout.css' %}">
            {% endblock %}

            {% block page_header %}
                <div class="container header-container">
                    <div class="row">
                        <div class="col"></div>
                    </div>
                </div>
            {% endblock %}

            {% block content %}
                <div class="overlay"></div>
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <hr>
                            <h2 class="logo-font mb-4">Thank You</h2>
                            <hr>
                            <p class="text-black">Your order information is below. A confirmation email will be sent to <strong>{{ order.email }}</strong>.</p>
                        </div>
                    </div>

                    <!-- order summary  -->
                    <div class="row">
                        <div class="col-12 col-lg-7"></div>
                    </div>
                    
                    <!-- deals etc  -->
                    <div class="row">
                        <div class="col-12 col-lg-7 text-right">
                            <a href="{% url 'products' %}?category=new_arrivals,deals,clearance" class="btn btn-black rounded-0 my-2">
                                <span class="icon mr-2">
                                    <i class="fas fa-gifts"></i>
                                </span>
                                <span class="text-uppercase">Now check out the latest deals!</span>
                            </a>
                        </div>
                    </div>
                </div>
            {% endblock %}

* Check signals are working
    * go to checkout/__init__.py

                default_app_config = 'checkout.apps.CheckoutConfig'

* Go to models.py (checkout)
    * add or 0 to the update total so if we manually delete the items the value is set to 0, not none

            self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0


[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 8 - add order summary </summary>

[ci video](https://youtu.be/KfA1GSBfozQ)

Checkout_success.html

             <!-- order summary  -->
            <div class="row">
                <div class="col-12 col-lg-7">
                    <!-- border for section  -->
                    <div class="order-confirmation-wrapper p-2 border">

                    <!-- order info  -->

                        <div class="row">
                            <div class="col">
                                <small class="text-muted">Order Info:</small>
                            </div>
                        </div>

                        <div class="row">
                            <!-- 1 row with 2 columns taking up 1/3 and 2/3 respectively -->
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Order Number</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.order_number }}</p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Order Date</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.date }}</p>
                            </div>
                        </div>

                    <!-- order details  -->

                        <div class="row">
                            <div class="col">
                                <small class="text-muted">Order Details:</small>
                            </div>
                        </div>

                        <!-- We need a for loop to make a new line for each item in the order  -->
                        <!-- lineitems here comes from the related_name attribute on the order field od the orderlineitem model  -->
                        {% for item in order.lineitems.all %}
                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="small mb-0 text-black font-weight-bold">
                                    {{ item.product.name }}{% if item.product_size %} - Size {{ item.product.size|upper }}{% endif %}
                                </p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="small mb-0">{{ item.quantity }} @ ${{ item.product.price }} each</p>
                            </div>
                        </div>
                        {% endfor %}

                    <!-- delivering to  -->

                        <div class="row">
                            <div class="col">
                                <small class="text-muted">Delivering To:</small>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Full Name</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.full_name }}</p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Address 1</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.street_address1 }}</p>
                            </div>
                        </div>

                        {% if order.street_address2 %}
                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Address 2</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.street_address2 }}</p>
                            </div>
                        </div>
                        {% endif %}

                        {% if order.county %}
                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">County</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.county }}</p>
                            </div>
                        </div>
                        {% endif %}

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Town or City</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.town_or_city }}</p>
                            </div>
                        </div>

                        {% if order.postcode %}
                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Postal Code</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.postcode }}</p>
                            </div>
                        </div>
                        {% endif %}

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Country</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.country }}</p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Phone Number</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.phone_number }}</p>
                            </div>
                        </div>

                    <!-- billing info  -->
                        <div class="row">
                            <div class="col">
                                <small class="text-muted">Billing Info:</small>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Order Total</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.order_total }}</p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Delivery</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.delivery_cost }}</p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-12 col-md-4">
                                <p class="mb-0 text-black font-weight-bold">Grand Total</p>
                            </div>
                            <div class="col-12 col-md-8 text-md-right">
                                <p class="mb-0">{{ order.grand_total }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 9 - add page loading </summary>

[ci video](https://youtu.be/kaSEjVz-8Pc)


checkout success.html

    * wrap optional form fields in if statements so they're only displayed if required  
        - street address 2  
        - county  
        - postcode  

Give your checkout success a whirl to see if it works  

Checkout.html

    * Add spinning overlay to  show page is loading 

                <div id="loading-overlay">
                    <h1 class="text-light logo-font loading-spinner">
                        <span class="icon">
                            <i class="fas fa-3x fa-sync-alt fa-spin"></i>
                        </span>
                    </h1>
                </div>

checkout.css

    * Add spinning css 

                #loading-overlay {
                    display: none;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(23, 162, 184, .85);
                    z-index: 9999;
                }

                .loading-spinner {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                    height: 100%;
                }


stripe elements.js

    * Use js to trigger overlay

                    $('#payment-form').fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);

Test it again and your page loader should appear when you submit form

    * 4000 0027 6000 3184 
    * This number can be used as a test with authentication

[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 10 - webhooks</summary>

[ci video](https://youtu.be/AU0F2wnrbEs)

At this point, there is a risk that if the user closes the browser before the form is submitted that payment is taken but no order is placed  
We need to build in some redundancy  
Each time an event occurs on stripe such as a payment intent being created, a payment being completed and so on, stripe sends out what's called a webhook we can listen for  
Webhooks are like the signals django sends each time a model is saved or deleted, except that they're sent securely from stripe to a URL we specify.

Create webhook handler

* create webhook_handler.py in checkout

                from django.http import HttpResponse

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
                            content=f'Webhook received: {event["type"]}',
                            status=200)



[Back to top](#walkthrough-steps)
</details>

<br>

**note for the following section:**  
Changes to the Stripe webhook creation page  
Stripe appears to be AB testing their webhook creation page since this video was created. The result of this is you may or may not see the "Receive All Events" option from this video.
If this affects you, please select just two webhooks from the list: payment_intent_succeeded and payment_intent_failed

<br>

<details>
<summary>Part 11 - Creat success/fail webhook handlers</summary>

[video](https://youtu.be/HsOrCqVovmk)


Create webhook handlers for payment which succeed / fail 

            def handle_payment_intent_succeeded(self, event):
            """
            Handle the payment_intent.succeeded webhook from Stripe
            This is sent each time the user completes the payment process
            """
            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200)

        def handle_payment_intent_payment_failed(self, event):
            """
            Handle the payment_intent.payment_failed webhook from Stripe
            """
            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200)

Get the handlers to listen:

* Go to urls.py in checkout app

                path('wh/', webhook, name='webhook'),
        
        import webhooks

                from .webhooks import webhook

recent webhook documentation [here](https://stripe.com/docs/payments/handling-payment-events) - the following is copied from Matt's video 

* Create webhooks.py at same level as urls.py

                from django.conf import settings
                from django.http import HttpResponse
                from django.views.decorators.http import require_POST
                from django.views.decorators.csrf import csrf_exempt

                from checkout.webhook_handler import StripeWH_Handler

                import stripe

                @require_POST
                @csrf_exempt
                def webhook(request):
                    """Listen for webhooks from Stripe"""
                    # Setup
                    wh_secret = settings.STRIPE_WH_SECRET
                    stripe.api_key = settings.STRIPE_SECRET_KEY

                    # Get the webhook data and verify its signature
                    payload = request.body
                    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
                    event = None

                    try:
                        event = stripe.Webhook.construct_event(
                        payload, sig_header, wh_secret
                        )
                    except ValueError as e:
                        # Invalid payload
                        return HttpResponse(status=400)
                    except stripe.error.SignatureVerificationError as e:
                        # Invalid signature
                        return HttpResponse(status=400)
                    except Exception as e:
                        return HttpResponse(content=e, status=400)


Settings.py - create stripe webhook environment variable

        STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

Run the server  
Copy the url and go to the stripe dashboard  
* Developers
* Webhooks
* Add endpoint
    * Copy in url, adding 'checkout/wh/ to the end of it
    * Select all events to be received 
    * click add endpoint
    * reveal and copy the signing secret
    * Export it
        * export STRIPE_WH_SECRET = copy_in_notes
    * Add to gitpod variables and restart workspace
* Send test webhook and it should work  



[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 12 - more event handlers </summary>

[ci video](https://youtu.be/OIueBHJcPM8)

Add more event handlers 

        # Set up a webhook handler
                    handler = StripeWH_Handler(request)

                    # Map webhook events to relevant handler functions
                    event_map = {
                        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
                        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
                    }

                    # Get the webhook type from Stripe
                    event_type = event['type']

                    # If there's a handler for it, get it from the event map
                    # Use the generic one by default
                    event_handler = event_map.get(event_type, handler.handle_event)

                    # Call the event handler with the event
                    response = event_handler(event)
                    return response


[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 13 - create database objects in database objects</summary>

[ci video](https://youtu.be/h0_abBkUPAw)

*Before we get to the webhook code we need to make a small addition to the stripe elements javascript. Basically since the payment intent.succeeded webhook will be coming from stripe and not from our own code into the webhook handler, we need to somehow stuff the form data into the payment intent object so we can retrieve it once we receive the webhook. Most of this we can do by simply adding the form data to the confirmed card payment method.*

Add shipping and billing details to handle form submit on js 

        payment_method: {
                        card: card,
                        billing_details: {
                            name: $.trim(form.full_name.value),
                            phone: $.trim(form.phone_number.value),
                            email: $.trim(form.email.value),
                            address: {
                                line1: $.trim(form.street_address1.value),
                                line2: $.trim(form.street_address2.value),
                                city: $.trim(form.town_or_city.value),
                                country: $.trim(form.country.value),
                                state: $.trim(form.county.value),
                            }
                        }
                    },
                    shipping: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        address: {
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            postal_code: $.trim(form.postcode.value),
                            state: $.trim(form.county.value),
                        }
                    },

Write a view to handle if customer wants their details saved in checkout/views.py

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

    Do your imports at the top

            HttpResponse
            from django.views.decorators.http import require_POST
            import json


        
[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 14 - connect js to view with webhook handler</summary>

*Add checkout form data caching in paymennt intent*

*In this video, you'll learn how to pass customer information through a stripe payment intent as metadata. There are many reasons developers may want to do this but in our case, we're doing it to ensure that all orders are entered into our database even in the event of a user error during the checkout process.*

[ci video](https://youtu.be/dewcliXUY8Y)

Create URL to access cache_checkout_data view

* checkout/views.py 

            path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),

Go to javascript and create new variables

* checkout/static/js
    
             // boolean of checked box by checking it's checked attribute 
            var saveInfo = Boolean($('#id-save-info').attr('checked'));

            // From using {% csrf_token %} in the form
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

            // create a small object to pass this information to the new view and also
            // pass the client secret for the payment intent
            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            };

            // create variable for new url 
            var url = '/checkout/cache_checkout_data/';

    Wrap the confirmcardpayment function in a post method and a done response

            // post data to view and when that's done call the confirmcardpayment function
            $.post(url, postData).done(function () {
            // Call confirm card payment method 
                stripe.confirmCardPayment(clientSecret, {
                   
                   ...

                    } else {
                        // If the status of payment intent comes back as succeeded, submit the fprm 
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });

**EXPLANATION OF FORM SUBMIT JAVASCRIPT**
[VIDEO LINK](https://youtu.be/dewcliXUY8Y?t=184)

When the user clicks the submit button the event listener prevents the form from submitting
and instead disables the card element and triggers the loading overlay.
Then we create a few variables to capture the form data we can't put in
the payment intent here, and instead post it to the cache_checkout_data view
The view updates the payment intent and returns a 200 response, at which point we
call the confirm card payment method from stripe and if everything is ok
submit the form.
If there's an error in the form then the loading overlay will
be hidden the card element re-enabled and the error displayed for the user.
If anything goes wrong posting the data to our view. We'll reload the page and
display the error without ever charging the user.

<br>

* webhook_handler.py
    * Add intent coming from stripe to payment_intent_succeeded

                intent = event.data.object
                print(intent)

Run your server and submit an order to see if it all works 

[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 15 - checking if order exists and responding appropriately</summary>

[ci video](https://youtu.be/TWeK8klQq00)

*In this video, we'll finalize the code from the previous video and test it out. In the payment intent succeeded webhook handler we've already got the payment intent which has all our customers information in it. All we need to do is use it to create an order just like we did with the form. The only reason we're doing this is in case the form isn't submitted for some reason like if the user closes the page on the loading screen.*

Webhook_handler.py

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
        # replace any empty strings in the shipping details with none since stripe will store them as blank strings which is not the same as the null value we want in the database.
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

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
                If the order is found we set order exists to true
                order_exists = True
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








[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 16</summary>

[ci video](https://youtu.be/lhYghsip36k)

*Sometimes there can be a delay in server time so we need to add a delay before creating orders if they're not found immediately*

 * webhook handler
    * This is actually the attept = 1 while < 5 bit in code from previous video (I used source code)
    * So the webhook will try find the order 5 times over 5 seconds before giving up and creating the order

If a user places an identical order more than once, only one would be found. So we need to alter the order model.

* checkout/models.py

            original_bag = models.TextField(null=False, blank=False, default='')
            stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    * Original bag is a text field that will contain the original shopping bag that created it.
    * Stripe_pid is a character field that will contain the stripe payment intent id

* migrate changes

            python3 manage.py makemigrations --dry-run
            python3 manage.py makemigrations
            python3 manage.py migrate --plan
            python3 manage.py migrate 

* Add fields to admin

            readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid')

            fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid)

* Update view to add these fields when form is submitted
    * first go to checkout.html
        * add hidden input containing client secret

                        <!-- PAYMENT FIELDSET  -->
                        <fieldset class="px-3">
                            <legend class="fieldset-label small text-black px-2 w-auto">Payment</legend>
                            <!-- A Stripe card element will go here -->
                            <div class="mb-3" id="card-element"></div>

                            <!-- Used to display form errors -->
                            <div class="mb-3 text-danger" id="card-errors" role="alert"></div>

                            <!-- Pass the client secret to the view so we can get the payment intent id -->
                            <input type="hidden" value="{{ client_secret }}" name="client_secret">
                        </fieldset>

    * views.py in checkout to get it if the order form is valid

                order_form = OrderForm(form_data)
                # If form is valid, save the order 
                if order_form.is_valid():
                    # commit stops multiple saves
                    order = order_form.save(commit=False)
                    # get payment intent id
                    pid = request.POST.get('client_secret').split('_secret')[0]
                    # we've already got the shopping bag here so adding that to the model is simple.
                    # we'll just dump it to a JSON string, set it on the order, and then we can save the order.
                    order.stripe_pid = pid
                    order.original_bag = json.dumps(bag)
                    order.save()


To remove all doubt as to whether we're looking for the proper order in the webhook handler, let's add the shopping bag and the stripe pid to the list of attributes we want to match on when finding it.

* webhook_handler.py 

            grand_total=grand_total,
            original_bag=bag,
            stripe_pid=pid,

    * Do imports

                from .models import Order, OrderLineItem
                from products.models import Product
                import json
                import time


[Back to top](#walkthrough-steps)
</details>


<details>
<summary>Part 17</summary>


[video url](https://youtu.be/mSNLcnTh618)

Make a test purchase and check webhook response to make sure it all still works  
It should. If it doesn't try the following:  
* Check your secret wh key is being used (echo $STRIPE_WH_SECRET)
* If not, save it to your variables and make sure scope is git_username/*
* Ensure there aren't any typos
* eu number in gitpod url and webhook address are the same
* 8000 port is public

Go to js file and comment out form submission and make another purchase.
This simulates either a user who closed the page before the form was submitted
but after the payment was confirmed or something else that went wrong
causing the form not to be submitted.


[Back to top](#walkthrough-steps)

</details>

<hr>


## Profile App

<details>
<summary>Open me</summary>

<details>
<summary>Part 1 - alter checkout page a smidge</summary>

* Rearrange form order to be more logical 

            {{ order_form.phone_number | as_crispy_field }}
            {{ order_form.street_address1 | as_crispy_field }}
            {{ order_form.street_address2 | as_crispy_field }}
            {{ order_form.town_or_city | as_crispy_field }}
            {{ order_form.county | as_crispy_field }}
            {{ order_form.postcode | as_crispy_field }}
            {{ order_form.country | as_crispy_field }}

* In forms.py change placeholder of county

            'county': 'County, State or locality',

* Shipping country must be two letter code which can be confusing. Change that to dropdown.

            pip3 install django_countries
            pip3 freeze > requirements.txt

    * models.py 

                from django_countries.fields import CountryField

                country = CountryField(blank_label='Country *', null=False, blank=False)
    
    * Migrate change

                python3 manage.py makemigrations --dry-run
                python3 manage.py makemigrations 
                python3 manage.py migrate --plan
                python3 manage.py migrate 

    * Runserver, navigate to checkout page and make sure it works - it should

* Grey out the text if a country isn't selected

    * checkout css

                select,
                select option {
                    color: #000000;
                }

                select:invalid,
                select option[value=""] {
                    color: #aab7c4 !important;
                }

* Remove placeholder in form for country (forms.py)

    * Remove country from placeholder dictionary
    * Alter the placeholder code below that 

                # Set cursor to start in full name when page loads 
                self.fields['full_name'].widget.attrs['autofocus'] = True
                # Go through the list
                for field in self.fields:
                    if field != 'country':
                        # If the field is required, add a star 
                        if self.fields[field].required:
                            placeholder = f'{placeholders[field]} *'
                        else:
                            placeholder = placeholders[field]
                        # set placeholder values as per above
                        self.fields[field].widget.attrs['placeholder'] = placeholder
                    # Add the css class we haven't created yet
                    self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                    # Remove labels
                    self.fields[field].label = False


* Create app for profiles

        python3 manage.py startapp profiles

* Add it to installed apps in settings.py

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 2 - create user profile model and basic profile template</summary>

The profile app will serve two purposes: 

1. Provide a user with a place to save default delivery information.
2. Provide them with a record of their order history.

To do that we'll need:

* a user profile model which is attached to the logged-in user.
* to attach the user's profile to all their orders.

* Create profile model

            from django.db import models
            from django.contrib.auth.models import User
            from django.db.models.signals import post_save
            from django.dispatch import receiver

            from django_countries.fields import CountryField


            class UserProfile(models.Model):
                """
                A user profile model for maintaining default
                delivery information and order history
                """
                # one to one specifies each user can only have one profile and vice versa
                user = models.OneToOneField(User, on_delete=models.CASCADE)
                # info grabbed from order model - made default and optional
                default_phone_number = models.CharField(max_length=20, null=True, blank=True)
                default_country = CountryField(blank_label='Country *', null=True, blank=True)
                default_postcode = models.CharField(max_length=20, null=True, blank=True)
                default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
                default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
                default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
                default_county = models.CharField(max_length=80, null=True, blank=True)

                def __str__(self):
                    return self.user.username

        This doesn't need to be in a separate signals.py file because there's only one signal.

            # This is here so that each time a user object is saved. We'll automatically 
            # either create a profile for them if the user has just been created, or just 
            # save the profile to update it if the user already existed.
            @receiver(post_save, sender=User)
            def create_or_update_user_profile(sender, instance, created, **kwargs):
                """
                Create or update the user profile
                """
                if created:
                    UserProfile.objects.create(user=instance)
                # Existing users: just save the profile
                instance.userprofile.save()

* Go to order model (checkout/models.py) to attached user profile to it

            from profiles.models import UserProfile

            # Link to user profiles
            # models.SET_NULL allows us to keep order history in the admin
            # field can be null or blank so users without accounts can still make purchases
            user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                            null=True, blank=True, related_name='orders')


* Migrate changes

        python3 manage.py makemigrations --dry-run
        python3 manage.py makemigrations 
        python3 manage.py migrate --plan
        python3 manage.py migrate 

* Create basic view

        from django.shortcuts import render

        def profile(request):
            """ Display the user's profile. """

            template = 'profiles/profile.html'
            context = {}

            return render(request, template, context)

* Create url for that view

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.profile, name='profile')
        ]

    * Include these urls in project urls.py file

            path('profile/', include('profiles.urls')),

* Create profile template

        {% extends "base.html" %}
        {% load static %}

        {% block extra_css %}
            <link rel="stylesheet" href="{% static 'profiles/css/profile.css' %}">
        {% endblock %}

        {% block page_header %}
            <div class="container header-container">
                <div class="row">
                    <div class="col"></div>
                </div>
            </div>
        {% endblock %}

        {% block content %}
            <div class="overlay"></div>
            <div class="container">
                <div class="row">
                    <div class="col">
                        <hr>
                        <h2 class="logo-font mb-4">My Profile</h2>
                        <hr>
                    </div>
                </div>
        {% endblock %}

* Create blank profile.css

* Test you can see the blank profile page by running the server and going to /profile


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 3 - fix allauth layout issues </summary>


* Go to root level templates folder - allaith - accounts - base.html

    * Add content

                {% extends "base.html" %}

                {% block content %}
                    <div class="container header-container">
                        <div class="overlay"></div>
                        <div class="row">
                            <div class="col-12 col-md-6">
                                <div class="allauth-form-inner-content">
                                    {% block inner_content %}
                                    {% endblock %}
                                </div>
                            </div>
                        </div>
                    </div>
                {% endblock %}

* Go to login.html and change block content to block inner_content

        {% block inner_content %}

    * Also use crispy forms to render the form, make header a h2, and custom classes, some hr rules and add a home button

                {% extends "account/base.html" %}

                {% load i18n %}
                {% load account socialaccount %}

                {% block head_title %}{% trans "Sign In" %}{% endblock %}

                {% block inner_content %}

                <hr>
                <h2 class="logo-font mb-4">{% trans "Sign In" %}</h2>
                <hr>

                {% get_providers as socialaccount_providers %}

                {% if socialaccount_providers %}
                <p>{% blocktrans with site.name as site_name %}Please sign in with one
                of your existing third party accounts. Or, <a href="{{ signup_url }}">sign up</a>
                for a {{ site_name }} account and sign in below:{% endblocktrans %}</p>

                <div class="socialaccount_ballot">

                <ul class="socialaccount_providers">
                    {% include "socialaccount/snippets/provider_list.html" with process="login" %}
                </ul>

                <div class="login-or">{% trans 'or' %}</div>

                </div>

                {% include "socialaccount/snippets/login_extra.html" %}

                {% else %}
                <p>{% blocktrans %}If you have not created an account yet, then please
                <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}</p>
                {% endif %}

                <form class="login" method="POST" action="{% url 'account_login' %}">
                {% csrf_token %}
                {{ form|crispy }}
                {% if redirect_field_value %}
                <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
                {% endif %}
                <a class="btn btn-outline-black rounded-0" href="{% url 'home' %}">Home</a>
                <button class="primaryAction" type="submit">{% trans "Sign In" %}</button>
                <p class="mt-2">
                    <a class="button secondaryAction" href="{% url 'account_reset_password' %}">{% trans "Forgot Password?" %}</a>
                </p>
                </form>

                {% endblock %}

* Make the following changes to all files in the account folder

    * Replace all the headers to match the one in the login template.
    * Anywhere there's a Content block I'll replace it with inner content.
    * Render all the forms that are currently form._p with crispy forms.
    * Add home or back buttons where appropriate.


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 4 - add CSS and wire up links for login and profiles </summary>

[ci video](https://youtu.be/MwIhHxez4Jo)

* Add css for allauth in base css file

        /* Allauth form formatting */

        .allauth-form-inner-content p {
            margin-top: 1.5rem; /* mt-4 */
            color: #6c757d; /* text-secondary */
        }

        .allauth-form-inner-content input {
            border-color: #000;
            border-radius: 0;
        }

        .allauth-form-inner-content label:not([for='id_remember']) {
            display: none;
        }

        .allauth-form-inner-content input::placeholder {
            color: #aab7c4;
        }

        .allauth-form-inner-content button,
        .allauth-form-inner-content input[type='submit'] {
            /* btn */
            display: inline-block;
            font-weight: 400;
            color: #fff;
            text-align: center;
            vertical-align: middle;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            background-color: #000;
            border: 1px solid #000;
            padding: .375rem .75rem;
            font-size: 1rem;
            line-height: 1.5;
            border-radius: 0;

            /* standard bootstrap btn transitions */
            transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
        }

        .allauth-form-inner-content button:hover,
        .allauth-form-inner-content input[type='submit']:hover {	
            color: #fff;
            background-color: #222;
            border-color: #222;
        }

        .allauth-form-inner-content a {
            color: #17a2b8; /* text-info */
        }


        input[name='q']::placeholder {
        color: #aab7c4;
        }

**Note** If you try to sign in now, it won't work because your code is trying to save the profile as it doesn't exist. Let's temporarily change the signal (in models.py) so it creates a profile.

        @receiver(post_save, sender=User)
        def create_or_update_user_profile(sender, instance, created, **kwargs):
            """
            Create or update the user profile
            """
            # if created:
            UserProfile.objects.create(user=instance)
            # Existing users: just save the profile
            # instance.userprofile.save()

If you try login now it should work. Reset the signal

        @receiver(post_save, sender=User)
        def create_or_update_user_profile(sender, instance, created, **kwargs):
            """
            Create or update the user profile
            """
            if created:
                UserProfile.objects.create(user=instance)
            # Existing users: just save the profile
            instance.userprofile.save()

* test registration process
    * Test emails are logged to the console so go there to get the confirmation link
    * You should be able to register then log in at this point

* Let's make the profile links work 

    * Update base template to link to profiles

            <a href="{% url 'profile' %}" class="dropdown-item">My Profile</a>

    * Update profiles/views.py

                from django.shortcuts import render, get_object_or_404
                from .models import UserProfile

                def profile(request):
                    """ Display the user's profile. """
                    profile = get_object_or_404(UserProfile, user=request.user)

                    template = 'profiles/profile.html'
                    context = {
                        'profile': profile,
                    }

                    return render(request, template, context)

    * Go to profile template and render the profile

            {{ profile }}


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 5 - Build user profile form</summary>

[ci video](https://youtu.be/NQxmvrqpSr0)

* Create forms.py in profiles app

            from django import forms
            from .models import UserProfile

            class UserProfileForm(forms.ModelForm):
                class Meta:
                    model = UserProfile
                    exclude = ('user',)

                def __init__(self, *args, **kwargs):
                    """
                    Add placeholders and classes, remove auto-generated
                    labels and set autofocus on first field
                    """
                    super().__init__(*args, **kwargs)
                    placeholders = {
                        # add default to the front to match model 
                        'default_phone_number': 'Phone Number',
                        'default_postcode': 'Postal Code',
                        'default_town_or_city': 'Town or City',
                        'default_street_address1': 'Street Address 1',
                        'default_street_address2': 'Street Address 2',
                        'default_county': 'County, State or Locality',
                    }

                    self.fields['default_phone_number'].widget.attrs['autofocus'] = True
                    for field in self.fields:
                        if field != 'default_country':
                            if self.fields[field].required:
                                placeholder = f'{placeholders[field]} *'
                            else:
                                placeholder = placeholders[field]
                            self.fields[field].widget.attrs['placeholder'] = placeholder
                        self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
                        self.fields[field].label = False

* Go to profile view and import the form

            from .forms import UserProfile

    * Update view

            def profile(request):
          
                form = UserProfileForm(instance=profile)
                orders = profile.orders.all()

                template = 'profiles/profile.html'
                context = {
                    'form': form,
                }

                return render(request, template, context)

* Render form on profile template

            {% extends "base.html" %}
            {% load static %}

            {% block extra_css %}
                <link rel="stylesheet" href="{% static 'profiles/css/profile.css' %}">
            {% endblock %}

            {% block page_header %}
                <div class="container header-container">
                    <div class="row">
                        <div class="col"></div>
                    </div>
                </div>
            {% endblock %}

            {% block content %}
                <div class="overlay"></div>
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <hr>
                            <h2 class="logo-font mb-4">My Profile</h2>
                            <hr>
                        </div>
                    </div>
                    
                    <div class="row">

                        <!-- default delivery info  -->

                        <div class="col-12 col-lg-6">
                            <p class="text-muted">Default Delivery Information</p>
                            <form class="mt-3" action="{% url 'profile' %}" method="POST" id="profile-update-form">
                                {% csrf_token %}
                                {{ form|crispy }}
                                <button class="btn btn-black rounded-0 text-uppercase float-right">Update Information</button>
                            </form>
                        </div>

                        <!-- order history -->

                        <div class="col-12 col-lg-6">
                            <p class="text-muted">Order History</p>
                            {{ orders }}
                        </div>
                    </div>
            {% endblock %}


* Edit userprofile model a tad 

        # one to one specifies each user can only have one profile and vice versa
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        # info grabbed from order model - made default and optional
        default_phone_number = models.CharField(max_length=20, null=True, blank=True)
        default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
        default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
        default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
        default_county = models.CharField(max_length=80, null=True, blank=True)
        default_postcode = models.CharField(max_length=20, null=True, blank=True)
        default_country = CountryField(blank_label='Country', null=True, blank=True)

* Add colour css to the form in profile css

        #profile-update-form .form-control {
            color: #000;
        }

        #profile-update-form input::placeholder {
            color: #aab7c4;
        }


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 6 - fix country colour on profile form </summary>

[ci video](https://youtu.be/PfYcZwN3OqU)

* Make the country grey by default, black when selected 

    * profile css

            #id_default_country,
            #id_default_country option:not(:first-child) {
                color: #000;
            }

            #id_default_country option:first-child {
                color: #aab7c4;
            }

    * profile.html - add js

                {% block postloadjs %}
                    {{ block.super }}
                    <script type="text/javascript" src="{% static 'profiles/js/countryfield.js' %}"></script>
                {% endblock %}

        * Create profile js file

                    // get value of country field when page loads and store it in variable 
                    let countrySelected = $('#id_default_country').val();
                    // Use boolean to see if option is selected or empty string 
                    if(!countrySelected) {
                        // if its not Selected, make it grey 
                        $('#id_default_country').css('color', '#aab7c4');
                    };
                    // capture the change event 
                    $('#id_default_country').change(function() {
                        // get the value of the box each time it changes 
                        countrySelected = $(this).val();
                        // if it's not selected mak it grey 
                        if(!countrySelected) {
                            $(this).css('color', '#aab7c4');
                        // if it is selected make it black 
                        } else {
                            $(this).css('color', '#000');
                        }
                    });

                
* Write post handler for profile view

    * profile/views.py

            if request.method == 'POST':
                form = UserProfileForm(request.POST, instance=profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully')
                else:
                    messages.error(request, 'Update failed. Please ensure the form is valid.')
            else:
                form = UserProfileForm(instance=profile)


When you update profile info and there's stuff in the basket, your basket is displayed with the success message. We don't want that.  

* profile / views.py
    * Add this to context
        
        'on_profile_page': True

* templates/includes/toasts/toast_success.html

    * change 

            {% if grand_total %}
        
        to

            {% if grand_total and not on_profile_page %}



[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 7 - add user's order history to profile </summary>

[ci video](https://youtu.be/ZdSH6hh8i3s)

* Add order history to profile.html

            <div class="col-12 col-lg-6">
                <p class="text-muted">Order History</p>
                <!-- create a small bootstrap table  -->
                <div class="order-history table-responsive">
                    <table class="table table-sm table-borderless">
                        <thead>
                            <tr>
                                <th>Order Number</th>
                                <th>Date</th>
                                <th>Items</th>
                                <th>Order Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for order in orders %}
                                <tr>
                                    <td>
                                        <!-- disply 6 numbers only, but show full with hover  -->
                                        <a href="{% url 'order_history' order.order_number %}"
                                        title="{{ order.order_number }}">
                                            {{ order.order_number|truncatechars:6 }}
                                        </a>
                                    </td>
                                    <td>{{ order.date }}</td>
                                    <td>
                                        <!-- unordered, unstyled list  -->
                                        <ul class="list-unstyled">
                                            <!-- For each item in the orders list of line-items  -->
                                            {% for item in order.lineitems.all %}
                                                <li class="small">
                                                    <!-- product size, name and quantity  -->
                                                    {% if item.product.has_sizes %}
                                                        Size {{ item.product.size|upper }}
                                                    {% endif %}{{ item.product.name }} x{{ item.quantity }}
                                                </li>
                                            {% endfor %}
                                        </ul>
                                    </td>
                                    <td>${{ order.grand_total }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

* Add css for max height in case user has a lot of orders

        .order-history {
            max-height: 416px; /* height of profile form + submit button */
            overflow-y: auto;
        }

* Create order_history view in profiles/views.py

        Import order model

                from checkout.models import Order

        def order_history(request, order_number):
        # get the order 
        order = get_object_or_404(Order, order_number=order_number)

        # Add message to tell user they're looking at a past order confirmation
        messages.info(request, (
            f'This is a past confirmation for order number {order_number}. '
            'A confirmation email was sent on the order date.'
        ))

        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
            # add the variable from_profile to check in that template if the user got there via the order history view
            'from_profile': True,
        }

        return render(request, template, context)

* Create url for it

        path('order_history/<order_number>', views.order_history, name='order_history'),

* checkout_success.html
    * If user came from their profile page, send them back to it instead of showing latest deals at the end

              <div class="row">
                <div class="col-12 col-lg-7 text-right">
                    {% if from_profile %}
                        <a href="{% url 'profile' %}" class="btn btn-black rounded-0 my-2">
                            <span class="icon mr-2">
                                <i class="fas fa-angle-left"></i>
                            </span>
                            <span class="text-uppercase">Back to Profile</span>
                        </a>
                    {% else %}
                        <a href="{% url 'products' %}?category=new_arrivals,deals,clearance" class="btn btn-black rounded-0 my-2">
                            <span class="icon mr-2">
                                <i class="fas fa-gifts"></i>
                            </span>
                            <span class="text-uppercase">Now check out the latest deals!</span>
                        </a>
                    {% endif %}
                </div>
            </div>


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 8 - Save details to profile and use them to auto fill checkout form </summary>

[ci video](https://youtu.be/F76YNC1Z4Bg)

* Add user profile to order admin fields

        fields = ('order_number', 'user_profile', 'date', 'full_name',


* checkout/views.py update checkout success 

        # We already know the form has been submitted and the order has been successfully processed at this point,
        # so this is a good place to add the user profile to it.
        if request.user.is_authenticated:
            # get the user's profile 
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the order
            order.user_profile = profile
            # save it 
            order.save()

            # Save the user's info if box was checked
            if save_info:
                profile_data = {
                    # these keys match the user profile model 
                    'default_phone_number': order.phone_number,
                    'default_country': order.country,
                    'default_postcode': order.postcode,
                    'default_town_or_city': order.town_or_city,
                    'default_street_address1': order.street_address1,
                    'default_street_address2': order.street_address2,
                    'default_county': order.county,
                }
                # Create an instance of the user profile form using the profile 
                # data, telling it we're going to update the profile we've obtained above.
                user_profile_form = UserProfileForm(profile_data, instance=profile)
                # if the form is valid, save it 
                if user_profile_form.is_valid():
                    user_profile_form.save()

    Do imports

            from profiles.models import UserProfile
            from profiles.forms import UserProfileForm

* test it works by first making sure there's no information in user profile, and then completing an order with the save info box checked. It should work!

* Lets use their delivery info to pre-fill form on checkout view

    * checkout/views.py 

            if request.user.is_authenticated:
                try:
                    # get their profile
                    profile = UserProfile.objects.get(user=request.user)
                    # use initial to pre-fill the fields 
                    order_form = OrderForm(initial={
                        'full_name': profile.user.get_full_name(),
                        'email': profile.user.email,
                        'phone_number': profile.default_phone_number,
                        'country': profile.default_country,
                        'postcode': profile.default_postcode,
                        'town_or_city': profile.default_town_or_city,
                        'street_address1': profile.default_street_address1,
                        'street_address2': profile.default_street_address2,
                        'county': profile.default_county,
                    })
                # if user is not authenticated, render a blank form 
                except UserProfile.DoesNotExist:
                    order_form = OrderForm()
            else:
                # create empty instance of order form
                order_form = OrderForm()

    * Test this worked by making a new order

**NOTE**
If you don't see the full name and email address filled out, make sure you've gotthem filled out on your user account in the admin.  
It really would be ideal to add fields to update those on the profile also.  
But in the interest of time, we'll skip that part as the process would be pretty much the same as what we've already done.  


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 9 - let webhooks handle user profiles too in case views fail </summary>

[ci video](https://youtu.be/-p2TIPJACrY)

* checkout/webhook_handler.py

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


Since we've already got their profile and if they weren't logged in it will just be none.
We can simply add it to their order when the webhook creates it.
In this way, the webhook handler can create orders for both authenticated users by attaching their profile.
And for anonymous users by setting that field to none.

* Just add this line for creating orders in the webhook handler 

            user_profile=profile,

* Import model at the top
        
        from profiles.models import UserProfile

* Test to make sure it works by commenting out form submission in checkout js

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 10 - send users an order confirmation email</summary>

[ci video](https://youtu.be/GDibdNzuhSQ)


* Create email files in checkout templates

* Create email subject file

        Boutique Ado Confirmation for Order Number {{ order.order_number }}

* Create email body file 

            Hello {{ order.full_name }}!

            This is a confirmation of your order at Boutique Ado. Your order information is below:

            Order Number: {{ order.order_number }}
            Order Date: {{ order.date }}

            Order Total: ${{ order.order_total }}
            Delivery: ${{ order.delivery_cost }}
            Grand Total: ${{ order.grand_total }}

            Your order will be shipped to {{ order.street_address1 }} in {{ order.town_or_city }}, {{ order.country }}.

            We've got your phone number on file as {{ order.phone_number }}.

            If you have any questions, feel free to contact us at {{ contact_email }}.

            Thank you for your order!

            Sincerely,

            Boutique Ado


* go to webhook_handler file

            def _send_confirmation_email(self, order):
            """Send the user a confirmation email"""
                cust_email = order.email
                subject = render_to_string(
                    'checkout/confirmation_emails/confirmation_email_subject.txt',
                    {'order': order})
                body = render_to_string(
                    'checkout/confirmation_emails/confirmation_email_body.txt',
                    {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
                
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [cust_email]
                )        

    don't forget the imports

            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.conf import settings

    Add the call to send the mail after payment

                self._send_confirmation_email(order)

* add email as default in settings.py

            DEFAULT_FROM_EMAIL = 'boutiqueado@example.com'

* Test it by making a purchase
</details>

[Back to top](#walkthrough-steps)
</details>

<hr>


## PRODUCT ADMIN


<details>
<summary>Part 1 - product form</summary>

[ci video](https://youtu.be/EeLC_22xs8Q)

We want store owners to be able to add products from the front end 

* Create forms.py in products app 

            from django import forms
            from .models import Product, Category


            class ProductForm(forms.ModelForm):

                class Meta:
                    model = Product
                    fields = '__all__'

                # over ride the init method to make changes to the fields 
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    categories = Category.objects.all()
                    # After getting all the categories, create a list of tuples of the 
                    # friendly names associated with their category ids using list
                    # comprehension. This is just a shorthand way of creating a for loop that adds items to a list.
                    friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

                    # Use friendly names instead of id
                    self.fields['category'].choices = friendly_names
                    # Add style classes to all fields
                    for field_name, field in self.fields.items():
                        field.widget.attrs['class'] = 'border-black rounded-0'

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 2- Add product view </summary>

[ci video](https://youtu.be/hWZdxrDVzG8)

* Add add_product view to products/views.py

                def add_product(request):
                    """ Add a product to the store """
                    form = ProductForm()
                    template = 'products/add_product.html'
                    context = {
                        'form': form,
                    }

                    return render(request, template, context)

    Import the form

                from .forms import ProductForm

* Create url for it
         
           path('add/', views.add_product, name='add_product'),

* Set product detail url as an integer 

            path('<int:product_id>/', views.product_detail, name='product_detail'),

* Create add products template

            {% extends "base.html" %}
            {% load static %}

            {% block page_header %}
                <div class="container header-container">
                    <div class="row">
                        <div class="col"></div>
                    </div>
                </div>
            {% endblock %}

            {% block content %}
                <div class="overlay"></div>
                <div class="container">

                    <!-- page title  -->

                    <div class="row">
                        <div class="col-12 col-md-6">
                            <hr>
                            <h2 class="logo-font mb-4">Product Management</h2>
                            <h5 class="text-muted">Add a Product</h5>
                            <hr>
                        </div>
                    </div>

                    <!-- Add product form -->

                    <div class="row">
                        <div class="col-12 col-md-6">
                            <!-- You need the enctype (encoding) to properly handle images  -->
                            <form method="POST" action="{% url 'add_product' %}" class="form mb-2" enctype="multipart/form-data">
                                {% csrf_token %}
                                {{ form | crispy }}
                                <!-- form buttons  -->
                                <div class="text-right">
                                    <a class="btn btn-outline-black rounded-0" href="{% url 'products' %}">Cancel</a>
                                    <button class="btn btn-black rounded-0" type="submit">Add Product</button>
                                </div>
                            </form>
                        </div>            
                    </div>
                </div>
            {% endblock %}


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 3 - Finish add product functionality</summary>

[ci video](https://youtu.be/JAQDbErhPiw)

* Write post handler for add_products view

    * products/views.py - add_product

                def add_product(request):
                    """ Add a product to the store """
                    # post handler
                    if request.method == 'POST':
                        # Instantiate a new instance of the product form from request.post and
                        # include request.files to get the image of the product if one was submitted.
                        form = ProductForm(request.POST, request.FILES)
                        # If the form is valid, save it
                        if form.is_valid():
                            product = form.save()
                            messages.success(request, 'Successfully added product!')
                            return redirect(reverse('product_detail', args=[product.id]))
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

    * You should now be able to add products using the form. However, if you try to add it to your cart you get an error if an image wasn't uploaded. 

        * Go to templates/includes/toasts_success.html to choose whether or not to render the image

                    {% if item.product.image %}
                        <img class="w-100" src="{{ item.product.image.url }}" alt="{{ item.product.name }}">
                    {% else %}
                        <img class="w-100" src="{{ MEDIA_URL }}noimage.png">
                    {% endif %}
        
        * Go to bag.html and apply the same fix 

* Add a link to add product page in the base template and mobile top header

            {% if request.user.is_superuser %}
                <a href="{% url 'add_product' %}" class="dropdown-item">Product Management</a>
            {% endif %}


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 4 - Editing products</summary>

[video](https://youtu.be/oehqshMBnn4)

* Create edit_product.html

            {% extends "base.html" %}
            {% load static %}

            {% block page_header %}
                <div class="container header-container">
                    <div class="row">
                        <div class="col"></div>
                    </div>
                </div>
            {% endblock %}

            {% block content %}
                <div class="overlay"></div>
                <div class="container">
                    <div class="row">
                        <div class="col-12 col-md-6">
                            <hr>
                            <h2 class="logo-font mb-4">Product Management</h2>
                            <h5 class="text-muted">Edit a Product</h5>
                            <hr>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-12 col-md-6">
                            <form method="POST" action="{% url 'edit_product' product.id %}" class="form mb-2" enctype="multipart/form-data">
                                {% csrf_token %}
                                {{ form | crispy }}
                                <div class="text-right">
                                    <a class="btn btn-outline-black rounded-0" href="{% url 'products' %}">Cancel</a>
                                    <button class="btn btn-black rounded-0" type="submit">Update Product</button>
                                </div>
                            </form>
                        </div>            
                    </div>
                </div>
            {% endblock %}

* Create view for edit_product

            def edit_product(request, product_id):
                """ Edit a product in the store """
                product = get_object_or_404(Product, pk=product_id)
                if request.method == 'POST':
                    form = ProductForm(request.POST, request.FILES, instance=product)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Successfully updated product!')
                        return redirect(reverse('product_detail', args=[product.id]))
                    else:
                        messages.error(request, 'Failed to update product. Please ensure the form is valid.')
                else:
                    # display prefilled form 
                    form = ProductForm(instance=product)
                    messages.info(request, f'You are editing {product.name}')

                template = 'products/edit_product.html'
                context = {
                    'form': form,
                    'product': product,
                }

                return render(request, template, context)

* Add url for the view

            path('edit/<int:product_id>/', views.edit_product, name='edit_product'),


You should be able to edit items with the manual url ( /products/edit/1 )


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 5 - Deleting products</summary>

[video](https://youtu.be/mm1smaUeisU)

* Create url for deleting (no template required )

            path('delete/<int:product_id>/', views.delete_product, name='delete_product'),


* Create delete view

            def delete_product(request, product_id):
                """ Delete a product from the store """
                product = get_object_or_404(Product, pk=product_id)
                product.delete()
                messages.success(request, 'Product deleted!')
                return redirect(reverse('products'))

You can now delete using the manual url ( /products/delete/product-id )

* Let's add edit and delete links 

    * On the product cards on all products page (products.html)
    * On the product detail page

                    {% if request.user.is_superuser %}
                        <small class="ml-3">
                            <a href="{% url 'edit_product' product.id %}">Edit</a> | 
                            <a class="text-danger" href="{% url 'delete_product' product.id %}">Delete</a>
                        </small>
                    {% endif %}

* Check they're now on the pages

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 6 - Securing the views</summary>

[ci video](https://youtu.be/u6tMGKEfX1k)

* Alter the product apps views.py

        import login required decorator

                from django.contrib.auth.decorators import login_required

        Add it to the add/edit/delete product views as a wrapper

* Do the same for the profile view

* Back to products/views.py

    * Only superusers have access to add/edit/delete views

            if not request.user.is_superuser:
                messages.error(request, 'Sorry, only store owners can do that.')
                return redirect(reverse('home'))


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 7 - Fixing the image (pt I)</summary>

[video](https://youtu.be/aQ0iYXzXOi8)

* Create widgets.py in products

            # import this file https://github.com/django/django/blob/main/django/forms/widgets.py
            from django.forms.widgets import ClearableFileInput
            # this is userd for translation
            from django.utils.translation import gettext_lazy as _

            # create a custom class which inherits from the original one
            class CustomClearableFileInput(ClearableFileInput):
                # override these settings
                clear_checkbox_label = _('Remove')
                initial_text = _('Current Image')
                input_text = _('')
                template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'

* Create the template described above

            <!-- Edit from here https://github.com/django/django/blob/main/django/forms/templates/django/forms/widgets/clearable_file_input.html -->
            {% if widget.is_initial %}
                <p>{{ widget.initial_text }}:</p>
                <a href="{{ widget.value.url }}">
                    <img width="96" height="96" class="rounded shadow-sm" src="{{ widget.value.url }}">
                </a>
                {% if not widget.required %}
                    <div class="custom-control custom-checkbox mt-2">
                        <input class="custom-control-input" type="checkbox" name="{{ widget.checkbox_name }}" id="{{ widget.checkbox_id }}">
                        <label class="custom-control-label text-danger" for="{{ widget.checkbox_id }}">{{ widget.clear_checkbox_label }}</label>
                    </div>
                {% endif %}<br>
                {{ widget.input_text }}
            {% endif %}
            <span class="btn btn-black rounded-0 btn-file">
                Select Image <input id="new-image" type="{{ widget.type }}" name="{{ widget.name }}"{% include "django/forms/widgets/attrs.html" %}>
            </span>
            <strong><p class="text-danger" id="filename"></p></strong>

* Tell products/forms.py we wanna use these widget files

            from .widgets import CustomClearableFileInput

            image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Part 8 - Fixing the image (pt II)</summary>

[video](https://youtu.be/yAYDJjQHDjg)

* Add styling for custom widget to base.css 

                /* Product form  */

                .btn-file {
                    /* set overflow of span around file input */
                    position: relative;
                    overflow: hidden;
                }

                .btn-file input[type="file"] {
                    position: absolute;
                    top: 0;
                    right: 0;
                    min-width: 100%;
                    min-height: 100%;
                    opacity: 0;
                    cursor: pointer;
                }

                .custom-checkbox .custom-control-label::before {
                    border-radius: 0;
                    border-color: #dc3545;
                }

                .custom-checkbox .custom-control-input:checked~.custom-control-label::before {
                    background-color: #dc3545;
                    border-color: #dc3545;
                    border-radius: 0;
                }

    
* Add if statement to add and edit_product.html to only render 'image' label if it's not our custom widget

                    {% csrf_token %}
                    {% for field in form %}
                        {% if field.name != 'image' %}
                            {{ field | as_crispy_field }}
                        {% else %}
                            {{ field }}
                        {% endif %}
                    {% endfor %}

* Add js to the bottom of each file to tell user what image will be changed to 

            {% block postloadjs %}
                {{ block.super }}
                <script type="text/javascript">
                    $('#new-image').change(function() {
                        var file = $('#new-image')[0].files[0];
                        $('#filename').text(`Image will be set to: ${file.name}`);
                    });
                </script>
            {% endblock %}

[Back to top](#walkthrough-steps)
</details>

<hr>

## Deploy to heroku

<details>
<summary>Create the heroku app</summary>

**Notes**  
*Error fix*  
If you get the error below during the steps to deployment:

        django.db.utils.OperationalError: FATAL: role "somerandomletters" does not exist

Please run the following command in the terminal to fix it:

        unset PGHOSTADDR

*A note for creating your database if you didn't use fixtures*  
When you come to follow this process for your milestone project, you may not have used a fixtures file to populate your database like the instructor did.

If this is the case, manually re-creating your database when you come to deploy can take a considerable amount of time. Thankfully, there is a short process you can follow to download your local mysql database and then upload it to postgres:

* Make sure your manage.py file is connected to your mysql database
* Use this command to backup your current database and load it into a db.json file:
            ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
* Connect your manage.py file to your postgres database
* Then use this command to load your data from the db.json file into postgres:
            ./manage.py loaddata db.json


[ci video](https://youtu.be/6mv-Qp37X4I)

* Create heroku app
    * Go to heroku.com
    * Click 'new'
        * Create the app
        * Go to 'resources'
            * search 'heroku'
            * pick 'Heroku Postgres' and select the 'Hobby Dev - Free' option

* Install dj database url and psycopg2 to your gitpod environment

                pip3 install dj_database_url
                pip3 install psycopg2-binary
                pip3 freeze > requirements.txt

* Setup the store's new database 
    * settings.py
        
            import dj database url

            Replace default database setup

                    DATABASES = {'default': dj_database_url.parse('the_heroku_database_url')}

                To get the heroku database url go to your newly created heroku app -> Settings -> Reveal config vars -> Copy the DATABASE_URL value

* We need to do migrations to connect to postgres

            python3 manage.py showmigrations
            python3 manage.py migrate

* import product data

            python3 manage.py loaddata categories
            python3 manage.py loaddata products

* Create superuser 

            python3 manage.py createsuperuser

* Remove heroku database config and uncomment the original to database url doesn't end up in version control

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Deploy to heroku</summary>

[ci video](https://youtu.be/Tp2CU1qpgJo)
[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/c82c677a83756a84c24181ed124e50ad38de67cf)

* Add if statement in settings.py so that when our app is running on Heroku where the database URL environment variable will be defined.

        if 'DATABASE_URL' in os.environ:
            DATABASES = {
                'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
            }
        else:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }

* install gunicorn to act as the webserver

        pip3 install gunicorn
        pip3 freeze > requirements.txt

* Create procfile

        web: gunicorn boutique_ado.wsgi:application

* login to heroku

        heroku login -i

* Temporarily disable collect static

        heroku config:set DISABLE_COLLECTSTATIC=1 --app ci-boutique-ado-walkthrough

* Add heroku app to allowed hosts in settings.py

        ALLOWED_HOSTS = ['ci-boutique-ado-walkthrough.herokuapp.com', 'localhost']

* Setup your heroku app for remote pushing and push

        heroku git:remote -a ci-boutique-ado-walkthrough
        git push heroku main


If you run your heroku site now it should work (with no css)


* Go to heroku and set it to auto deploy when pushed

    * heroku app
        * Deploy
            * Deployment method -> github
                * Connect your github and search for your repo name
                * Connect that
                * Enable auto deploy further down the page

* Get a django secret key generator (<https://miniwebtool.com/django-secret-key-generator/>)
* Go to heroku -> settings -> Display config vars
    * SECRET_KEY
    * Paste in your secret key for the value

* Settings.py of environment
    * Get secret key from environment

                SECRET_KEY = os.environ.get('SECRET_KEY', '')
    
    * Only set debug to true while in development

                DEBUG = 'DEVELOPMENT' in os.environ

push your app and it should auto build on heroku

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Create aws account</summary>

CORS configuration

**Important**  
AWS updated their systems after this video was made and the code from the video above for the CORS configuration no longer works.

Please use the following code for your CORS configuration instead:

[
  {
      "AllowedHeaders": [
          "Authorization"
      ],
      "AllowedMethods": [
          "GET"
      ],
      "AllowedOrigins": [
          "*"
      ],
      "ExposeHeaders": []
  }
]


[ci video](https://youtu.be/uGdZeX319Q4)

* go to aws.amazon.com and create aws account
* Search for 's3' when logged in
* create bucket
    * Name it the same as your heroku app
    * Uncheck block all public access (needs to be public for static files)
    * acknowledge the bucket will be public
* Go to bucket
    * Properties
        * Static website hosting
            * Use to host website
            * Fill in defaults 
            * save
    * Permissions
        * CORS congifuration
            * Edit

                        [
                        {
                            "AllowedHeaders": [
                                "Authorization"
                            ],
                            "AllowedMethods": [
                                "GET"
                            ],
                            "AllowedOrigins": [
                                "*"
                            ],
                            "ExposeHeaders": []
                        }
                        ]

        * Bucket policy
            * Edit
                * Policy generator
                    * Type: s3 bucket policy
                    * Effect: Allow
                    *  Principal: *
                    * Action: Get object
                    * Copy ARN from bucket policy page and paste into generator page
                    * Click add statement
                    * Click generate policy
                    * Copy the policy and paste into edit box on policy page
                    * Add /* to the resource
                    * Save
        * Access control list
            * Edit
                * Public access -> list

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Create aws groups, policies, users</summary>

[ci video](https://youtu.be/BzzjLvC0Fcc)

With our s3 bucket ready to go. Now we need to create a user to access it.  
We can do this through another service called Iam which stands for Identity and Access Management.

* Go to aws and search 'IAM'  

    The process here is first we're going to create a group for our user to live in.
    Then create an access policy giving the group access to the s3 bucket we created.
    And finally, assign the user to the group so it can use the policy to access all our files.

    * Create a group
        * In IAM click 'user groups'
            * New group
            * Name it 'manage-boutique-ado" 
            * Create
        * Now go to 'policies'
            * Create policy
            * JSON tab
                * Click 'import managed policy'
                * Search s3
                * Click Amazons3FullAccess
                * Import
                * Nip back to s3 - permissions - bucket policy and copy the arn
                * Paste it in as so

                            "Resource": [
                                "arn:aws:s3:::ci-boutique-ado-walkthrough",
                                "arn:aws:s3:::ci-boutique-ado-walkthrough/*"
                            ]

                * Click next:tags
                * Click review policy
                * Give it a name and description
                * Click create policy
                * You'll be brought back to the list of policies
    * Add the policy to the group
         * Go to user groups
            * Select your recently made group
                * Go to permissions
                * Click add permissions button
                * Select attach policy
                * Find the one you just made
                * Click add permissions at the bottom
    * Create user to put into the group
        * Go to users
            * Click add user
                * Name: boutique-ado-staticfiles-user
                * access type: programmatic
                * Select Next: permissions
                    * Select the group we made
                    * Click next: tags
                    * Click next: Review
                    * Click create user
    * Download the csv file which contains secret keys  
    **Note** You cannot access these again so MAKE SURE THIS FILE IS SAVED


[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Connect django to s3</summary>

[ci video](https://youtu.be/r-HJv_MyOqw)
[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/2229819dd50d944117bfe9837c590d59d70bbc66)

* Install boto3 and django-storages

        pip3 install boto3
        pip3 install django-storages
        pip3 freeze > requirements.txt

* Add storages to installed apps in settings.py

        'storages',

* To connect Django to s3 add settings in settings.py to tell it which bucket it should be communicating with

        # CONNECTING DJANGO TO S3
        # check for environment variable called use_aws
        if 'USE_AWS' in os.environ:
            # Bucket Config
            AWS_STORAGE_BUCKET_NAME = 'ci-boutique-ado-walkthrough'
            AWS_S3_REGION_NAME = 'EU (Ireland) eu-west-1'
            AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

* GO to heroku and add AWS keys to config variables
    * AWS_ACCESS_KEY_ID : copied from csv from earlier
    * AWS_SECRET_ACCESS_KEY : copied from csv from earlier
    * USE_AWS: True
    * Remove disablestatic variable

* In settings.py tell django where static files are coming from in production

        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

* Create custom_storages.py at root

        from django.conf import settings
        from storages.backends.s3boto3 import S3Boto3Storage

        class StaticStorage(S3Boto3Storage):
            location = settings.STATICFILES_LOCATION

        class MediaStorage(S3Boto3Storage):
            location = settings.MEDIAFILES_LOCATION

* Set the locations in settings.py

        # Static and media files
        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        STATICFILES_LOCATION = 'static'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        MEDIAFILES_LOCATION = 'media'

* Override static and media urls 

        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'



[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Caching, media files and stripe</summary>

[ci video](https://youtu.be/JPb82nILolU)
[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/9ed36dc2c07228041b56b28174dd96ee56e6c59a)

* Add file caching to settings.py

            # Cache control - tells browser to cache files for a long time
            AWS_S3_OBJECT_PARAMETERS = {
                'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                'CacheControl': 'max-age=94608000',
            }

* Add media files to s3
    * Go to s3 on aws.com
        * Create folder called media
        * Upload files
        * Select all your project images from wherever they're saved
        * Select grant public read access
        * Upload

* Confirm email address for superuser on postgres database
    * Login to admin from heroku app
    * Verify email address of user and add as primary

* Add stripe keys to heroku config vars

    * login to stripe
    * Developers
    * Api keys
        * Copy publishable key
            * Go to heroku app - settings
            * Config vars
            * STRIPE_PUBLIC_KEY: paste
        * Copy secret key
            * heroku config vars
            * STRIPE_SECRET_KEY: paste

    * Create new webhook endpoint
        * Developers -> Webhooks
        * Add endpoint
        * Insert url for heroku app followed by /checkout/wh/
        * Listen to all events
        * Add endpoint
        * Reveal signing secret
        * Add to heroku config vars under STRIPE_WH_SECRET

**Remember** These variables need to match what's in settings.py

* Send test webhook from stripe - should be successful

**Notes**
If we wanted to turn this into a real store at this point it would involve some additional testing on stripe, setting up real confirmation emails and switching our stripe settings to use the live keys rather than the test ones we're using now.  
We would also likely want to write a plethora of tests for our application, in particular in the checkout and shopping bag app, and make some security adjustments as well as some minor changes to make it easier to work between our development and production environments seamlessly.

</details>

[Back to top](#walkthrough-steps)


<hr>

## Sending emails

<details>
<summary>with django</summary>

[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/a07c1ca5a3b973eb47e5c944829cea06ead3936d)  
[ci video](https://youtu.be/uCtLfAd6w-c)  

* Create 2 step verification for your email address
* Get a password for your django app
* Go to heroku app config vars
    * EMAIL_HOST_PASS : paste in password
    * EMAIL_HOST_USER : the email used above

* settings.py
    * Remove the backend email

            EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    * Add custom settings

            if 'DEVELOPMENT' in os.environ:
                EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
                DEFAULT_FROM_EMAIL = 'boutiqueado@example.com'
            else:
                EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                EMAIL_USE_TLS = True
                EMAIL_PORT = 587
                EMAIL_HOST = 'smtp.gmail.com'
                EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
                EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
                DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

* test using a real / fake email to register (temp mail)[https://temp-mail.org/en/]

</details>

[Back to top](#walkthrough-steps)

<hr>

## CODE REFACTORING

<details>
<summary>Base css, login and registration</summary>

[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/933797d5e14d6c3f072df31adf0ca6f938d02218)  
[video](https://youtu.be/xv5DJ16kg6U)

CSS ISSUES

            /* pad the top a bit when navbar is collapsed on mobile */
            @media (max-width: 991px) {
                .header-container {
                    padding-top: 116px;
                }

                body {
                    height: calc(100vh - 116px);
                }

                .display-4.logo-font.text-black {
                    font-size: 2rem;
                }

                .nav-link {
                    padding: 0.15rem;
                }

                .nav-link i.fa-lg {
                    font-size: 1rem;
                }

                .navbar-toggler {
                    padding: .6rem .6rem;
                    font-size: 1rem;
                }

                #delivery-banner h4 {
                    font-size: .9rem;
                }

                .btn.btn-outline-black.rounded-0,
                .btn.btn-black.rounded-0 {
                    padding: .375rem .375rem;
                }

                .btn.btn-outline-black.rounded-0.btn-lg,
                .btn.btn-black.rounded-0.btn-lg {
                    padding: .375rem .375rem;
                    font-size: .75rem;
                }

                .increment-qty, .decrement-qty {
                    padding: .25rem .5rem !important;
                }
            }

* Add profile url to mobile-top-header.html

* Give mobile users a way to get to the home page
    * main-nav.html

                <!-- Home button for mobile  -->
                <li class="nav-item d-block d-md-none">
                    <a class="logo-font font-weight-bold nav-link text-black mr-5" href="{% url 'home' %}" id="home-link">
                        Home
                    </a>
                </li>

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Shopping bag</summary>

[video](https://youtu.be/l-F1ICBhk-Q)  
[source code](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/250e2c2b8e43cccb56b4721cd8a8bd4de6686546)

**IMPORTANT**  

Code issue  
After this video was made, we discovered an issue with a part of the code. The minus quantity button in the bag is meant to be disabled when the quantity hits 1. Which works on small screens after this refactor. However, this does not work on larger screens.

The reason for this is because during this code refactoring, the instructor uses the quantity-form twice, and hides one or the other depending on the screen size. However, as the quantity-form uses an ID to identify itself, only the first element within the HTML with that ID is picked up by the corresponding code. Even though you can only see one form at a time in the browser, they both exist within the HTML.

You don't need to fix this error while working on this walkthrough project. However please be aware of this if you want to include similar functionality in your own project.

To fix this issue you would need to change the ID on the quantity-form to a class, and refactor the JavaScript to look for elements with the same class name and perform the appropriate actions.

<hr>

To make the bag better we're gonna change it to a grid instead of a table for mobiles only

* Create individual files for each table section 

    * bag-total.html
    * checkout-buttons.html
    * product-image.html
    * product-info.html
    * quantity-form.html

* Copy each section from bag.html to the corresponding file
* Change each block to an include statement

<details>
<summary>Reveal new bag.html</summary>

        {% extends "base.html" %}
        {% load static %}
        {% load bag_tools %}

        {% block page_header %}
            <div class="container header-container">
                <div class="row">
                    <div class="col"></div>
                </div>
            </div>
        {% endblock %}

        {% block content %}
            <div class="overlay"></div>
            <div class="container mb-2">
                <div class="row">
                    <div class="col">
                        <hr>
                        <h2 class="logo-font mb-4">Shopping Bag</h2>
                        <hr>
                    </div>
                </div>

                <div class="row">
                    <div class="col">
                        {% if bag_items %}
                            <div class="d-block d-md-none">
                                <div class="row">
                                    <div class="col">
                                        {% include "bag/bag-total.html" %}
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        {% include "bag/checkout-buttons.html" %}
                                        <p class="text-muted mb-5">A summary of your bag contents is below</p>
                                    </div>
                                </div>
                                {% for item in bag_items %}
                                    <div class="row">
                                        <div class="col-12 col-sm-6 mb-2">
                                            {% include "bag/product-image.html" %}
                                        </div>
                                        <div class="col-12 col-sm-6 mb-2">
                                            {% include "bag/product-info.html" %}
                                        </div>
                                        <div class="col-12 col-sm-6 order-sm-last">
                                            <p class="my-0">Price Each: ${{ item.product.price }}</p>
                                            <p><strong>Subtotal: </strong>${{ item.product.price | calc_subtotal:item.quantity }}</p>
                                        </div>
                                        <div class="col-12 col-sm-6">
                                            {% include "bag/quantity-form.html" %}
                                        </div>
                                    </div>
                                    <div class="row"><div class="col"><hr></div></div>
                                {% endfor %}
                                <div class="btt-button shadow-sm rounded-0 border border-black">
                                    <a class="btt-link d-flex h-100">
                                        <i class="fas fa-arrow-up text-black mx-auto my-auto"></i>
                                    </a>	
                                </div>
                            </div>
                            <div class="table-responsive rounded d-none d-md-block">
                                <table class="table table-sm table-borderless">
                                    <thead class="text-black">
                                        <tr>
                                            <th scope="col">Product Info</th>
                                            <th scope="col"></th>
                                            <th scope="col">Price</th>
                                            <th scope="col">Qty</th>
                                            <th scope="col">Subtotal</th>
                                        </tr>
                                    </thead>

                                    {% for item in bag_items %}
                                        <tr>
                                            <td class="p-3 w-25">
                                                {% include "bag/product-image.html" %}
                                            </td>
                                            <td class="py-3">
                                                {% include "bag/product-info.html" %}
                                            </td>
                                            <td class="py-3">
                                                <p class="my-0">${{ item.product.price }}</p>
                                            </td>
                                            <td class="py-3 w-25">
                                                {% include "bag/quantity-form.html" %}
                                            </td>
                                            <td class="py-3">
                                                <p class="my-0">${{ item.product.price | calc_subtotal:item.quantity }}</p>
                                            </td>
                                        </tr>
                                    {% endfor %}
                                    <tr>
                                        <td colspan="5" class="pt-5 text-right">
                                            {% include "bag/bag-total.html" %}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="5" class="text-right">
                                            {% include "bag/checkout-buttons.html" %}
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        {% else %}
                            <p class="lead mb-5">Your bag is empty.</p>
                            <a href="{% url 'products' %}" class="btn btn-outline-black rounded-0 btn-lg">
                                <span class="icon">
                                    <i class="fas fa-chevron-left"></i>
                                </span>
                                <span class="text-uppercase">Keep Shopping</span>
                            </a>
                        {% endif %}
                    </div>
                </div>
            </div>
        {% endblock %}

        {% block postloadjs %}
        {{ block.super }}
        <script type="text/javascript">
            $('.btt-link').click(function(e) {
                window.scrollTo(0,0)
            })
        </script>
        {% include 'products/includes/quantity_input_script.html' %}

        <script type="text/javascript">
            // Update quantity on click
            $('.update-link').click(function(e) {
                var form = $(this).prev('.update-form');
                form.submit();
            })

            // Remove item and reload on click
            $('.remove-item').click(function(e) {
                var csrfToken = "{{ csrf_token }}";
                var itemId = $(this).attr('id').split('remove_')[1];
                var size = $(this).data('product_size');
                var url = `/bag/remove/${itemId}/`;
                var data = {'csrfmiddlewaretoken': csrfToken, 'product_size': size};

                $.post(url, data)
                .done(function() {
                    location.reload();
                });
            })
        </script>
        {% endblock %}

</details>

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Flake8 and python</summary>

[ci video](https://youtu.be/pty5AlktsZo)  

View all problems in code instead of viewing all files

        python3 -m flake8

ctrl + click on the error to go to it

</details>

[Back to top](#walkthrough-steps)


<hr>
