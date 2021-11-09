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

## Shopping bag

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

[Back to top](#walkthrough-steps)
</details>

<hr>