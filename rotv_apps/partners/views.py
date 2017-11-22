# -*- coding: utf-8 -*-
# Create your views here.
from django.views import generic

from .forms import MediaPatronageForm
from .models import MediaPatronage


class MediaPatronageRequestView(generic.CreateView):
    model = MediaPatronage
    form_class = MediaPatronageForm
