## Prime Pix Studio

Prime Pix Studio is a photography and videography company focused on events related to dance. This repository contains the code for its website, made with the [Django](https://github.com/django/django) framework and the [nanogallery2](https://nanogallery2.nanostudio.org/) image gallery. This project is ongoing and being continously developed upon. It is licensed under the AGPL V3 license.

## Installation
Create a modified settings file, likely as `pps/local_settings.py` which copies all of the existing settings with `from settings import *` and sets `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` set for payments.

```sh
$ pip install -r requirements.txt
$ python manage.py migrate --settings=pps.local_settings
$ python manage.py runserver --settings=pps.local_settings`
```
