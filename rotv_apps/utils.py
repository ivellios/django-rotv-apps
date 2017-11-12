# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from tinymce.models import HTMLField


EnhancedTextField = HTMLField if 'tinymce' in settings.INSTALLED_APPS else models.TextField
