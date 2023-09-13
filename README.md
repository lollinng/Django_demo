Steps:

1) Create an env
2) Activate it : env\Scripts\activate.ba
3) Download django project : django-admin startproject demo
4) Create django application
    i) cd django project : cd demo
    ii) python manage.py startapp myapp
    ii) link the app to main project in settings.py of mainproject
5) In app add routing fuction inside View.py  
6) Create a new file urls.py and import the routing function from views.py in it
7) Create urls pattern dict in url and add path of routing function
8) Link craeted application url to the main project in urls.py file
9) run the server using :  python manage.py runserver
10) Create templates folder inside the application file and put your html file inside it


MIGRATE: 
python manage.py makemigrations
python manage.py migrate