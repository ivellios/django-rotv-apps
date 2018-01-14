# Django ROTV apps

[![Build Status](https://travis-ci.org/ivellios/django-rotv-apps.svg?branch=master)](https://travis-ci.org/ivellios/django-rotv-apps)

This package is a group of Django apps for running web tv website service.

## Our story

Originally this package was created for [Raport Obieżyświata](http://raportobiezyswiata.tv>) - a leading web tv channel in Poland dedicated to sci-fi and fantasy news reporting, book reviews and conventions recaps.

Since the very begining the work of our group, we were working voluntarily to provide the best quality videos for the Polish Fandom. Thus we decided to release our source code of the website to provide others with tools for creating their own great project.

## Language note

This project was created only for Polish region. Thus the verbose names for the fields are in Polish. In the future we plan to provide English as a base language for the package.

## How to use this package

The full documentation for the package is due to be created.

# Installation

You can easily install this package with `pip`. Preferably you will use _virtualenv_ for that

```bash
$ pip install git+ssh://git@github.com/ivellios/django-rotv-apps.git
```

## Optional TinyMCE fields

This app uses another package with TinyMCE v4 for part of `TextFields`. It is included in the installation optional requirements. 
If you plan on using the package simply install it with:

```bash
$ pip install git+ssh://git@github.com/ivellios/django-rotv-apps.git[tinymce]
```

**Remember** that `django-tinymce4-lite` package may colide with other tinymce apps installed in your virtualenv.

# Configuration

After that you can add your apps to your project. In your `settings` file add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'tinymce', # add this one if you will use django-tinemce4-lite package
    # ...
    'rotv_apps.blog',
    'rotv_apps.heros',
    'rotv_apps.navigations',
    'rotv_apps.partners',
    'rotv_apps.program',
    'rotv_apps.tag_search',
]
```

## TinyMCE configuration

`django-tinymce4-lite` package is optional, but recommended for use with this app. The package is compatible
with `django-grappelli` and `django-filebrowser`. If you plan to use them together, remember to put `tinymce` in 
`INSTALLED_APPS` **before** `filebrowser` since `django-tinymce4-lite` is overriding some of its templates.

## URLs configuration

Also include our `urls` to use it's defaults or create your own for the views.

```python
urlpatterns = [
    # your urls go here...
    url(r'', include('rotv_apps.urls')),
    # and there...
]
```

# Package development

To develop the package simply clone it from GitHub and install while in the main dir with

```
$ pip install -e .
```

This will install the package in the _editable_ mode, so you can change the code and test it during the development.

# Testing

Most of the code is covered by tests. You can run them with:

```
$ python setup.py test
```

You can also test compatibility with different versions of the python and django by running `tox`. Mind that tox needs to be installed globally along with python 2.7, 3.5 and 3.6 to run this tests.

```
$ tox
```

# Contributing

If you wish to join us and develop the package and the service together with us, feel free to contact us at [redakcja@raportobiezyswiata.tv](mailto:redakcja@raportobiezyswiata.tv). Also you can always create a new Issue for enhancement or Pull Request here at GitHub. They all will be very welcome.

# Changelog

**2.2.3:**
- added email notification for new events added
- activation of event logged with date/time
- added created/modified for event (MediaPatronage)
- added action to admin for bulk activation of events
