# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MediaPatronageQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def before(self, date):
        return self.filter(start__lte=date)

    def after(self, date):
        return self.filter(end__gte=date)


class MediaPatronageManager(models.Manager):
    pass


class FutureMediaPatronageManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        qs = super(FutureMediaPatronageManager, self).get_queryset()
        return qs.active().after(timezone.now().date()).order_by('start')


class UpcomingMediaPatronageManager(FutureMediaPatronageManager):
    """
        Queryset of patronages that start before the end of the first one.
    """
    use_for_related_fields = True

    def get_queryset(self):
        patronages = super(UpcomingMediaPatronageManager, self).get_queryset()
        first_patronage = patronages.first()
        if first_patronage:
            return patronages.before(first_patronage.end)
        return patronages


class MediaPatronage(models.Model):
    """ Patronat wydarzenia """
    name = models.CharField(_(u'Nazwa własna'), max_length=255)
    logo = models.ImageField(_(u'Logotyp'),upload_to='logos/patronage')
    url = models.URLField(_(u'Adres url'),blank=True)
    active = models.BooleanField(_(u'Aktywny'), default = False)
    start = models.DateField(_(u'Start wydarzenia'))
    end = models.DateField(_(u'Koniec wydarzenia'))

    objects = MediaPatronageManager.from_queryset(MediaPatronageQuerySet)()
    future  = FutureMediaPatronageManager.from_queryset(MediaPatronageQuerySet)()
    upcoming = UpcomingMediaPatronageManager.from_queryset(MediaPatronageQuerySet)()

    class Meta:
        verbose_name = _(u'Patronat wydarzenia')
        verbose_name_plural = _(u'Patronaty wydarzeń')

    def __unicode__(self):
        return self.name


class NormalMediaPatronage(models.Model):
    """ Patronat wydawnictw, publikacji, produktow """
    name = models.CharField(_(u'Nazwa własna'), max_length=255)
    logo = models.ImageField(_(u'Logotyp'), upload_to='logos/patronage')
    url = models.URLField(_(u'Adres url'), blank=True)
    active = models.BooleanField(_(u'Aktywny'), default = False)
    start = models.DateField(_(u'Od kiedy wyświetlać'), blank=True, null=True)
    end = models.DateField(_(u'Do kiedy wyświetlać'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Patronat produktu')
        verbose_name_plural = _(u'Patronaty produktów')

    def __unicode__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(_(u'Nazwa własna'), max_length=255)
    logo = models.ImageField(_(u'Logotyp'),upload_to='logos/partner')
    url = models.URLField(_(u'Adres url'),blank=True)
    active = models.BooleanField(_(u'Aktywny'), default = False)

    class Meta:
        verbose_name = _(u'Partner')
        verbose_name_plural = _(u'Partnerzy')

    def __unicode__(self):
        return self.name


class MediaPatron(models.Model):
    name = models.CharField(_(u'Nazwa własna'), max_length=255)
    logo = models.ImageField(_(u'Logotyp'),upload_to='logos/patron')
    url = models.URLField(_(u'Adres url'),blank=True)
    active = models.BooleanField(_(u'Aktywny'), default = False)

    class Meta:
        verbose_name = _(u'Patron')
        verbose_name_plural = _(u'Patroni')

    def __unicode__(self):
        return self.name


class Colaborator(models.Model):
    name = models.CharField(_(u'Nazwa własna'), max_length=255)
    logo = models.ImageField(_(u'Logotyp'),upload_to='logos/colaborator')
    url = models.URLField(_(u'Adres url'),blank=True)
    active = models.BooleanField(_(u'Aktywny'), default = False)

    class Meta:
        verbose_name = _(u'Współpracujący')
        verbose_name_plural = _(u'Współpracujący')

    def __unicode__(self):
        return self.name
