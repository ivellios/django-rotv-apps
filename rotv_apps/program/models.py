# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.registry import register

from ..utils import EnhancedTextField


class Program(models.Model):
    name = models.CharField(_(u'Nazwa programu'), max_length=255, unique=True)
    slug = models.SlugField(_(u'Slug'), unique=True)
    image = models.ImageField(_(u'Obraz dla programu'), upload_to='programs', blank=True)
    desc = EnhancedTextField(_(u'Opis'), blank=True, null=True)
    order = models.IntegerField(_(u'Kolejność'), default=9999)
    new_tags = TagField(_(u'Tagi'), blank=True, null=True)

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
    name = models.CharField(_(u'Nazwa'), max_length=255)
    description = EnhancedTextField(_(u'Opis'), blank=True, null=True)
    image = models.ImageField(_(u'Zdjęcie'), upload_to='hosts', null=True, blank=True)
    email = models.EmailField(_(u'Adres e-mail'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Prowadzący')
        verbose_name_plural = _(u'Prowadzący')
        ordering = ['name', ]


class Playlist(models.Model):
    name = models.CharField(_(u'Name'), max_length=255)
    slug = models.SlugField(_(u'Slug'), unique=True)
    description = EnhancedTextField(_('Description'), blank=True, null=True)
    new_tags = TagField(_(u'Tags'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def sorted_episodes(self):
        return self.episodes.order_by('playlist_episodes')


class PlaylistEpisode(models.Model):
    episode_fk = models.ForeignKey('program.Episode', related_name='playlist_episodes')
    playlist_fk = models.ForeignKey('program.Playlist', related_name='playlist_episodes')
    position = models.PositiveSmallIntegerField(_('Position'), null=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.playlist.name


class EpisodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def before(self, date):
        return self.filter(publish_time__lt=date)

    def after(self, date):
        return self.filter(publish_time__gt=date)

    def get_next_to(self, episode):
        getit = False
        for ep in self:
            if getit:
                return ep
            if episode == ep:
                getit = True
        if getit:
            # This would happen when the last
            # item made getit True
            return self[0]
        return False

    def get_prev_to(self, episode):
        qs = self.reverse()
        return qs.get_next_to(episode)


class PublishedEpisodeManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(PublishedEpisodeManager, self).get_queryset().active().before(timezone.now())


class EpisodeManager(models.Manager):
    pass


class Episode(models.Model):
    added = models.DateTimeField(_(u'Data dodania'), auto_now_add=True)
    program = models.ForeignKey(Program, null=True, blank=True)
    playlist = models.ManyToManyField('program.Playlist', through='program.PlaylistEpisode')
    number = models.IntegerField(_(u'Numer odcinka'), blank=True, null=True)
    hosts = models.ManyToManyField(Host, verbose_name=_(u'Prowadzący'), blank=True,)
    title = models.CharField(_(u'Tytuł odcinka'), max_length=255)
    slug = models.SlugField(_(u'Slug'), unique=True)
    short = models.CharField(_(u'Krótki opis'), max_length=255)
    description = EnhancedTextField(_(u'Opis'))
    new_tags = TagField(_(u'Tagi'), blank=True, null=True)
    youtube_code = models.CharField(_(u'Kod YT'), max_length=255)
    image = models.ImageField(_(u'Ilustracja'), upload_to='episodes')
    promoted = models.BooleanField(_('Polecany'), default=False)
    active = models.BooleanField(_('Do publikacji?'), default=True,
                                 help_text=_(u'Niezależnie od daty publikacji film będzie opublikowany '
                                             u'tylko jeżeli ta opcja jest zaznaczona'))
    publish_time = models.DateTimeField(_('Publikacja'), default=timezone.now)

    objects = EpisodeManager.from_queryset(EpisodeQuerySet)()
    published = PublishedEpisodeManager.from_queryset(EpisodeQuerySet)()

    class Meta:
        verbose_name = _(u'Odcinek')
        verbose_name_plural = _(u'Odcinki')
        ordering = ['-publish_time', ]

    def __unicode__(self):
        return self.title + ' - ' + self.get_number()

    def get_absolute_url(self):
        if self.program:
            return reverse('program_episode_detail', args=[str(self.program.slug), str(self.slug)])
        else:
            return reverse('episode_detail', args=[str(self.slug)])

    def get_next_episode(self):
        if self.program:
            return Episode.published.filter(program=self.program).get_next_to(self)
        else:
            return None

    def get_previous_episode(self):
        if self.program:
            return Episode.published.filter(program=self.program).get_prev_to(self)
        else:
            return None

    def get_next_episode_in_program(self):
        if self.program:
            num = self.number + 1
            try:
                return Episode.published.get(program=self.program, number=num, )
            except Episode.DoesNotExist:
                pass
        return None

    def get_previous_episode_in_program(self):
        if self.program:
            num = self.number - 1
            try:
                return Episode.published.get(program=self.program, number=num, )
            except Episode.DoesNotExist:
                pass
        return None

    def get_number(self):
        return u"{} #{:01d}".format(self.program, self.number) if self.program and self.number else u""


register(Program)
register(Episode)
register(Playlist)
