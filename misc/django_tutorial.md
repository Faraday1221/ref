# Django Tutorial notes
learning django to support working with pysec. The tutorial we are working through is found [here](https://docs.djangoproject.com/en/1.9/intro/tutorial01/). The second tutorial spends time with the Django API and the third focused on Views.

## tutorial01

setting up the structure for the project looks something like

    $ django-admin startproject mysite

this creates the new directory "mysite" which is initialized with two files
    - manage.py
    - mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py

_note: all of this is explained in [tutorial01](https://docs.djangoproject.com/en/1.9/intro/tutorial01/)_

We primarily interact with django with the _manage.py_ file

To veryify that our Django project works, change into the outer mysite directory

    $ python manage.py runserver

this produces a warning about unapplied database migrations (we ignore for now)

what we have done with the following command is to  start the Django development server, a lightweight web server written purely in Python. **THIS IS A DEVELOPMENT ENVIORNMENT ONLY!** We can now visit the server described in the system check i.e.
http://127.0.0.1:8000/

This has the following message "It worked!" Congratulations on your first Django-powered page

We can now start building our first app in the mysite directory
$ python manage.py startapp polls

we then open the polls/views.py file and add a bit of code, then to call the view we need to map it to a URL - and for this we need a URLconf (which we create with the urls.py file in polls/urls.py)

Once we have created this file we now edit the mysite/urls.py file (dont get confused with the directory, there are now two urls.py files). This is called "pointing the rool URLconf at the polls.urls module." Truely I don't really get what this is doing. After making the changes we are told to make... we can then check that the index is "working as intended" by visiting localhost:8000/polls in our browser. Note that port 8000 is specified in the runserver as the last 4 digits (we can reconfig if necessary)


## tutorial02
 this starts with a nice explaination of how Django handles SQL
 we create the necessary database tables (in SQLite the defualt SQL included in Python, unless otherwise specified) using the following command (note this is from the mysite dir)

    $ python manage.py migrate

 This should have created the db.sqlite3 database

 We now create "models" essentiall, the database layout with additional metadata to do this we open the polls.models.py file and define two classes (the class functions as the table and the class variables - I can't recall the correct nomenclature for "class variables" - function as the field definitions for the table)

 We then have to update the mysite/settings.py file so it "knows" about the polls app. Once this is done we need to tell Django we have made changes to our models

Migrations are how Django stores changes to our models (and thus database schema) - they're just files on disk we can seen them under polls.migrations/0001_initial.py

There is a lot to be said about migrations (and the acompanying SQL) which we will skip here (see tutorial02) but there is a little cheat sheet worth capturing

- change models (in models.py)
- run python manage.py makemigrations to create migrations for those changes
- run python manage.py migrate to apply those changes to the database

(note: due to a spelling error I had to update the migration such that the updated migration is now 0002)

### Playing with the API
_There is a lot here, and not included in these notes_

### Django Admin

for this example I'm using
Username: admin
Email: admin@example.com
Password: <>


## tutorial03

### Views
Each page we might want to display on our web app is considered to be a view. **note: working notes incomplete**
