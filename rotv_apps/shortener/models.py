import base64
import hashlib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_short_hash():
    hash_base = timezone.now()
    hasher = hashlib.sha1(str(hash_base))
    hash_string = base64.urlsafe_b64encode(hasher.digest()[0:10]).replace('=', '')
    try:
        ShortenedURL.objects.get(slug=hash_string)
    except ShortenedURL.DoesNotExist:
        return hash_string
    else:
        return get_short_hash()


class ShortenedURL(models.Model):
    url = models.URLField(_('Original URL'), )
    slug = models.SlugField(_('Short URL slug'), default=get_short_hash, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, )
    modified = models.DateTimeField(_('Modified'), auto_now=True, )
    expires = models.DateTimeField(_('Expires'), blank=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), related_name='created_shortened_urls')
    modified_by = models.ForeignKey(User, verbose_name=_('Modified by'), related_name='modified_shortened_urls')

    class Meta:
        verbose_name = _('Shortened URL')
        verbose_name_plural = _('Shortened URLs')
        ordering = ['-modified', '-created']

    def get_absolute_url(self):
        return self.url

    def get_shortened_url(self):
        return '{}/{}'.format(
            settings.SHORTENER_BASE_URL,
            self.slug
        )
