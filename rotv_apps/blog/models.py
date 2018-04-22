# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..utils import EnhancedTextField

from tagging.fields import TagField
from tagging import registry


class CategoryQueryset(models.QuerySet):
    pass


class CategoryManager(models.Manager):
    pass


class Category(models.Model):
    name = models.CharField(_(u'Nazwa'), max_length=255)
    slug = models.SlugField(_(u'Adres/Slug'), unique=True)

    objects = CategoryManager.from_queryset(CategoryQueryset)

    class Meta:
        verbose_name = _(u'Kategoria')
        verbose_name_plural = _(u'Kategorie')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return 'id__iexact', 'name__icontains'


class EntryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def before(self, date):
        return self.filter(publish_time__lte=date)

    def after(self, date):
        return self.filter(publish_time__gte=date)

    def published(self):
        return self.active().before(timezone.now())


class EntryManager(models.Manager):
    pass


class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        return super(PublishedEntryManager, self).get_queryset().active().before(timezone.now())


class Entry(models.Model):

    ALIGN_CHOICES = (
        ('alignleft', _(u'Do lewej')),
        ('alignright', _(u'Do prawej')),
        ('aligncenter', _(u'Do środka'))
    )

    title = models.CharField(_(u'Tytuł'), max_length=255)
    slug = models.SlugField(_(u'Adres/Slug'), unique=True)
    text = EnhancedTextField(_(u'Tresc'))
    new_tags = TagField(_('Tagi'), blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_('Kategorie'))
    posted = models.DateTimeField(_(u'Utworzono'), auto_now_add=True)
    modified = models.DateTimeField(_(u'Zmieniono'), auto_now=True)
    active = models.BooleanField(_(u'Aktywny'),
                                 help_text=_(u'Zaznacz, jeżeli tekst jest gotowy do publikacji (nie notka)'),
                                 default=False)
    publish_time = models.DateTimeField(_('Czas publikacji'), default=timezone.now)
    image = models.ImageField(_(u'Obraz szeroki (cover)'), blank=True, null=True, upload_to='blog-images')
    image_right = models.ImageField(_(u'Obraz wąski/pływający'), blank=True, null=True, upload_to='blog-images')

    objects = EntryManager.from_queryset(EntryQuerySet)()
    published = PublishedEntryManager.from_queryset(EntryQuerySet)()

    class Meta:
        verbose_name = _(u'Wpis')
        verbose_name_plural = _(u'Wpisy')
        ordering = ['-publish_time', '-posted', '-pk']

    def __unicode__(self):
        return self.title

    def get_text_length(self):
        return len(self.text)

    def get_absolute_url(self):
        return reverse('blog_entry', kwargs={'year': str(self.posted.year),
                                             'month': str(self.posted.month),
                                             'slug': str(self.slug)})

    @cached_property
    def is_long(self):
        return len(self.text) > settings.LONG_ENTRY_LENGTH


registry.register(Entry)
