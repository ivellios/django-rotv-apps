# -*- coding: utf-8 -*-
# Create your views here.
from django.urls import reverse
from django.views import generic

from .forms import MediaPatronageForm
from .models import MediaPatronage


class MediaPatronageRequestView(generic.CreateView):
    model = MediaPatronage
    form_class = MediaPatronageForm

    def get_success_url(self):
        return reverse('event_request_confirm')


class MediaPatronageRequestConfirmView(generic.TemplateView):
    template_name = 'partners/confirm.html'
