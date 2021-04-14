## Fiduciam - Local Development Setup Guide

### Prerequisite

- #### Python 3.5 installed on your local development pc, because there is a package of django form builder that works with django 2, and python 3.5

### Steps to setup and run application on local development pc

- Once you in root project create virtual envirnoment

        python -m venv env

- Install dependencies

        pip install -r requirements.txt

- Run migrations

        python manage.py migrate

- Run local server

        python manage.py runserver

- Create super user

        python manage.py createsuperuser

- Login with your super user credentials:

        http://127.0.0.1:8000/admin/login/?next=/admin/

- Once you are there you can create users/ forms

- And assign those forms to users

- Run unit tests:

        python manage.py test food

- Run functional tests(Used SELENIUM frameworks, to automate browser testing)

        python manage.py test functional_tests

#### NOTE ON SELENIUM

- Used this chrome driver:

        chromedriver.exe

- That driver has to be compatible with local chrome version installed in your pc, if they dont match, selenium will throw the below error

        selenium.common.exceptions.SessionNotCreatedException:
        Message: session not created: This version of ChromeDriver only supports Chrome version 90
        Current browser version is 89.0.4389.114 with binary path

- To solve this, either make sure you have this chrome version installed

        89.0.4389.114

- Or go on below link to find the chromedriver that is is compatible with your local chrome version

        https://chromedriver.chromium.org/downloads
