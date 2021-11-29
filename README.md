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

        django.admin startproject boutique_ado .
    
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

## CHECKOUT APP
<details>
<summary>Open</summary>

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

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Templates and views pt 2</summary>

[Back to top](#walkthrough-steps)
</details>

<details>
<summary>Templates and views pt 3</summary>

</details>

[Back to top](#walkthrough-steps)
</details>