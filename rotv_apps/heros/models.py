# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class HeroQuerySet(models.QuerySet):
    pass


class HeroManager(models.Manager):
    pass


class Hero(models.Model):
    name    = models.CharField(_(u'Nazwa'), max_length=255, )
    slug    = models.SlugField(_(u'Część adresu'), )
    limit   = models.PositiveIntegerField(_(u'Ilość wyświetlanych elementów'), default=5)

    objects = HeroManager.from_queryset(HeroQuerySet)

    class Meta:
        verbose_name = _(u'Rotator')
        verbose_name_plural = _(u'Rotatory')
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def get_active_entries(self):
        return self.entries.filter(is_active=True)[:self.limit]


class HeroEntryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def before(self, date):
        return self.filter(publish_time__lte=date)

    def after(self, date):
        return self.filter(publish_time__gte=date)


class HeroEntryManager(models.Manager):
    pass


class PublishedHeroManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(PublishedHeroManager, self).get_queryset().active().before(timezone.now())


class HeroEntry(models.Model):
    hero            = models.ForeignKey(Hero, related_name='entries')
    title           = models.CharField(_(u'Tytuł'), max_length=255, )
    subtitle        = models.CharField(_(u'Podtytuł'), max_length=255, blank=True, null=True)
    text            = models.CharField(_(u'Lead'), max_length=255, blank=True, null=True)
    url             = models.CharField(_(u'URL do którego prowadzi'), max_length=200)
    button_text     = models.CharField(_(u'Przycisk dalej'), max_length=255, blank=True, null=True,
                                   default='Zobacz odcinek')
    image           = models.ImageField(_(u'Ilustracja'), upload_to='heros')
    sort            = models.IntegerField(_(u'Kolejność'), default=100)
    added           = models.DateTimeField(_(u'Dodano'), auto_now_add=True)
    modified        = models.DateTimeField(_(u'Zmodyfikowano'), auto_now=True)
    publish_time    = models.DateTimeField(_(u'Publikacja'), default=timezone.now)
    is_active       = models.BooleanField(_(u'Czy jest aktywny'), default=True)

    objects = HeroEntryManager.from_queryset(HeroEntryQuerySet)()
    published = PublishedHeroManager.from_queryset(HeroEntryQuerySet)()

    class Meta:
        verbose_name = _(u'Wpis w rotatorze')
        verbose_name_plural = _(u'Wpisy w rotatorach')
        ordering = ['sort', '-modified', 'title']

    def __unicode__(self):
        return self.title
