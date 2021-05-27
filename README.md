## Prime Pix Studio

Prime Pix Studio is a photography and videography company focused on events related to dance. This repository contains the code for its website, made with the [Django](https://github.com/django/django) framework and the [nanogallery2](https://nanogallery2.nanostudio.org/) image gallery. It is licensed under the AGPL V3 license.

## Installation
Create a modified settings file, likely as `pps/local_settings.py` which copies all of the existing settings with `from settings import *` and sets `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` for payments. For a simple development setup, do the following:

```sh
$ pip install -r requirements.txt
$ python manage.py migrate --settings=pps.local_settings
$ python manage.py runserver --settings=pps.local_settings`
```

For production deployment, see the [Deploying Django](https://docs.djangoproject.com/en/3.2/howto/deployment/) documentation.

## License

AGPLv3, see LICENSE.

Copyright (C) 2020-2021 Prime Pix Studio
