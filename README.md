## Prime Pix Studio [![Codacy Badge](https://api.codacy.com/project/badge/Grade/7e658e9b69994de08ef9c6f7dd5d848c)](https://app.codacy.com/manual/aviddev/pps-site?utm_source=github.com&utm_medium=referral&utm_content=TheAvidDev/pps-site&utm_campaign=Badge_Grade_Dashboard)

Prime Pix Studio is a photography and videography company focused on events related to dance. This repository contains the code for its website, made with the [Django](https://github.com/django/django) framework and the [nanogallery2](https://nanogallery2.nanostudio.org/) image gallery. This project is ongoing and being continously developed upon. It is licensed under the GPL V2 license.

## Dependancies
* [Python 3](https://www.python.org/).
* [Django Discord Integration](https://github.com/Ninjaclasher/django-discord-integration) or [my fork](https://github.com/TheAvidDev/django-discord-integration) of it.
* Python dependancies are in the [requirements.txt](https://github.com/TheAvidDev/django-discord-integration/blob/master/requirements.txt) file.

## Installation
* Clone the repository with `git clone https://github.com/TheAvidDev/pps-site.git`.
* (optional) Setup a `virtualenv` environment with `virtualenv [name]` and enter it `source [name]/bin/activate]` (linux) or `[name]\Scripts\activate` (windows).
* Install [Django Discord Integration](https://github.com/Ninjaclasher/django-discord-integration) or [my fork](https://github.com/TheAvidDev/django-discord-integration) of it, as per the instructions on their respective pages.
* Install python dependancies with `pip install -r requirements.txt`.
* Create a `local_settings.py` file inside of `pps/` which contains `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` variables as well as any personal configuration options.
* Run `python manage.py migrate --settings=pps.local_settings` to create the database.
* Run `python manage.py createsuperuser --settings=pps.local_settings` to create a superuser for the admin site.
* Run the website with `python manage.py runserver --nostatic --settings=pps.local_settings`.
* Visit the website at `127.0.0.1:8000`.
