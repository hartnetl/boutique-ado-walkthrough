![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Walkthrough steps

- [Workspace setup](#set-up-your-workspace)  
- [Authentication](#allauth-authentication)
- [Base template setup](#setup-base-template)
- [Home page template setup](#home-setup)

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
            <div class="container headeer-container">
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
</details>

<details>
<summary>Video 3</summary>
</details>

<details>
<summary>Video 4 - navigation</summary>
</details>

[Back to top](#walkthrough-steps)
</details>