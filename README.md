![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Walkthrough steps

- [Workspace setup](#set-up-your-workspace)  
- [Authentication](#allauth-authentication)

##

<details>
<summary></summary>

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

        path('accounts', include('allauth.urls')),

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










</details>