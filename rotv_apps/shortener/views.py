from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import RedirectView
from .models import ShortenedURL


class ShortenedURLRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'shortened-url-redirect'

    def get_redirect_url(self, *args, **kwargs):
        shortened_url = get_object_or_404(ShortenedURL, slug=kwargs['slug'])
        if not shortened_url.expires or shortened_url.expires >= timezone.now():
            return shortened_url.get_absolute_url()
        raise Http404
