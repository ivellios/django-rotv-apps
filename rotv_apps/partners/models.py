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


PATRONAGE_UPLOAD_DIR_LOGO = 'logos/patronage'
PATRONAGE_UPLOAD_DIR_BANNER = 'uploads/partners/banners'
PATRONAGE_UPLOAD_DIR_COVER = 'uploads/partners/covers'
PATRONAGE_UPLOAD_DIR_SMALL = 'uploads/partners/images'


class MediaPatronage(models.Model):
    """ Patronage for event model class. Keeps information on all events. """
    name = models.CharField(_(u'Nazwa wydarzenia'), max_length=255)
    logo = models.ImageField(_(u'Logo'), upload_to=PATRONAGE_UPLOAD_DIR_LOGO)
    url = models.URLField(_(u'Adres url strony internetowej'), blank=True)
    active = models.BooleanField(_(u'Aktywny patronat?'), default=False)
    start = models.DateField(_(u'Data początku'))
    end = models.DateField(_(u'Data zakończenia'))
    contact_email = models.EmailField(_(u'E-mail kontaktowy organizatora'), )
    city = models.CharField(_(u'Miasto'), max_length=128)
    spot = models.CharField(_(u'Miejsce wydarzenia'), max_length=255,
                            help_text=u'Dokładna nazwa szkoły, targów, lokacji',
                            blank=True)
    banner_image = models.ImageField(_(u'Baner wydarzenia'),
                                     help_text=u'Szerokość sugerowana: 800px',
                                     upload_to=PATRONAGE_UPLOAD_DIR_BANNER,
                                     blank=True, null=True)
    cover_image = models.ImageField(_(u'Szeroki obraz typu cover'),
                                    help_text=u"Szerokość sugerowana: 1000-1600px",
                                    upload_to=PATRONAGE_UPLOAD_DIR_COVER,
                                    blank=True, null=True)
    small_image = models.ImageField(_(u'Mały obrazk'),
                                    help_text=u'Szerokość sugerowana: 300px',
                                    upload_to=PATRONAGE_UPLOAD_DIR_SMALL,
                                    blank=True, null=True)
    additional_notes = models.TextField(_(u'Informacje dodatkowe'),
                                        help_text=u'Opis wydarzenia, charakter, grupa docelowa i inne.',
                                        blank=True)

    objects = MediaPatronageManager.from_queryset(MediaPatronageQuerySet)()
    future = FutureMediaPatronageManager.from_queryset(MediaPatronageQuerySet)()
    upcoming = UpcomingMediaPatronageManager.from_queryset(MediaPatronageQuerySet)()

    class Meta:
        verbose_name = _(u'Promowane wydarzenie')
        verbose_name_plural = _(u'Promowane wydarzenia')

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
        verbose_name = _(u'Promowany produkt')
        verbose_name_plural = _(u'Promowane produkty')

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

