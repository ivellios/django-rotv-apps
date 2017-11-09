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

After that you can add your apps to your project. In your `settings` file add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'tinymce',
    # ...
    'rotv_apps.blog',
    'rotv_apps.heros',
    'rotv_apps.navigations',
    'rotv_apps.partners',
    'rotv_apps.program',
    'rotv_apps.tag_search',
]
```

Also include our `urls` to use it's defaults or create your own for the views.

```python
urlpatterns = [
    # your urls go here...
    url(r'', include('rotv_apps.urls')),
    # and there...
]
```

### Note on TinyMCE

This app uses another package with TinyMCE v4 for `TextFields`. It is included in the installation requirements, so it
will be included in the installation. **Remember** that this package may overwrite your other tinymce apps installed in virtualenv.

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
