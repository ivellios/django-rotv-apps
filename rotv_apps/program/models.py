# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.registry import register


class Program(models.Model):
    name        = models.CharField(_(u'Nazwa programu'), max_length=255, unique=True)
    slug        = models.SlugField(_(u'Slug'))
    image       = models.ImageField(_(u'Obraz dla programu'), upload_to='programs', blank=True)
    desc        = models.TextField(_(u'Opis'), blank=True, null=True)
    order       = models.IntegerField(_(u'Kolejność'), default=9999)
    new_tags    = TagField(_(u'Tagi'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Program')
        verbose_name_plural = _(u'Programy')
        ordering = ['order']

    def __unicode__(self):
        return self.name

    def get_image(self):
        try:
            return self.published_episodes.order_by('-publish_time')[0].image
        except KeyError:
            return None

    def get_absolute_url(self):
        return reverse('program_detail', args=[self.slug])

    def get_episode_list(self):
        return self.published_episodes.order_by('-number')

    def get_episode_brief(self, limit=6):
        return self.published_episodes.order_by('-number')[:limit]

    def get_last_episode(self):
        try:
            return self.published_episodes.order_by('-number')[0]
        except IndexError:
            return None

    @property
    def published_episodes(self):
        return Episode.published.filter(program=self)


class Host(models.Model):
    name        = models.CharField(_(u'Nazwa'), max_length=255)
    description = models.TextField(_(u'Opis'), blank=True, null=True)
    image       = models.ImageField(_(u'Zdjęcie'), upload_to='hosts', null=True, blank=True)
    email       = models.EmailField(_(u'Adres e-mail'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Prowadzący')
        verbose_name_plural = _(u'Prowadzący')
        ordering = ['name', ]


class EpisodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def before(self, date):
        return self.filter(publish_time__lt=date)

    def after(self, date):
        return self.filter(publish_time__gt=date)


class PublishedEpisodeManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(PublishedEpisodeManager, self).get_queryset().active().before(timezone.now())


class EpisodeManager(models.Manager):
    pass


class Episode(models.Model):
    added           = models.DateTimeField(_(u'Data dodania'), auto_now_add=True)
    program         = models.ForeignKey(Program)
    number          = models.IntegerField(_(u'Numer odcinka'))
    hosts           = models.ManyToManyField(Host, verbose_name=_(u'Prowadzący'), blank=True,)
    title           = models.CharField(_(u'Tytuł odcinka'), max_length=255)
    short           = models.CharField(_(u'Krótki opis'), max_length=255)
    description     = models.TextField(_(u'Opis'))
    new_tags        = TagField(_(u'Tagi'), blank=True, null=True)
    youtube_code    = models.CharField(_(u'Kod YT'), max_length=255)
    image           = models.ImageField(_(u'Ilustracja'), upload_to='episodes')
    promoted        = models.BooleanField(_('Polecany'), default=False)
    active          = models.BooleanField(_('Do publikacji?'), default=True,
                                          help_text=_(u'Niezależnie od daty publikacji film będzie opublikowany '
                                                        u'tylko jeżeli ta opcja jest zaznaczona'))
    publish_time    = models.DateTimeField(_('Publikacja'), default=timezone.now)

    objects = EpisodeManager.from_queryset(EpisodeQuerySet)()
    published = PublishedEpisodeManager.from_queryset(EpisodeQuerySet)()

    class Meta:
        verbose_name = _(u'Odcinek')
        verbose_name_plural = _(u'Odcinki')
        ordering = ['-publish_time', ]
        unique_together = (('number', 'program'),)

    def __unicode__(self):
        return self.title + ' - ' + unicode(self.program) + ' #' + str(self.number)

    def get_absolute_url(self):
        return reverse('program_episode_detail', args=[str(self.program.slug),str(self.number)])

    def get_next_episode(self):
        num = self.number + 1
        try:
            return Episode.published.get(program=self.program, number=num, )
        except Episode.DoesNotExist:
            return None

    def get_previous_episode(self):
        num = self.number - 1
        try:
            return Episode.published.get(program=self.program, number=num, )
        except Episode.DoesNotExist:
            return None

    def get_next_url(self):
        e = self.get_next_episode()
        if e:
            return e.get_absolute_url()
        return None

    def get_previous_url(self):
        e = self.get_previous_episode()
        if e:
            return e.get_absolute_url()
        return None

    def get_number(self):
        return "{} #{:01d}".format(self.program, self.number)

register(Program)
register(Episode)
