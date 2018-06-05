# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..heros.models import HeroEntry, Hero
from .models import Episode, Program, Host, PlaylistEpisode, Playlist


class PlaylistEpisodeModelOptions(admin.TabularInline):
    fields = ['episode', 'playlist', 'position', ]
    model = PlaylistEpisode
    raw_id_fields = ('episode', )
    autocomplete_lookup_fields = {
        'm2m': ['episode'],
    }
    extra = 3

    def get_extra(self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class SortablePlaylistEpisodeModelOptions(PlaylistEpisodeModelOptions):
    fields = ['episode', 'playlist', 'position', 'episode_slug']
    sortable_field_name = 'position'
    readonly_fields = ['episode_slug']


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'program', 'active', 'publish_time', 'promoted', 'short', ]
    list_filter = ['program', 'publish_time', ]
    actions = ['make_hero_from_episode', 'publish', ]
    prepopulated_fields = {'slug': ('title',), }
    inlines = [
        PlaylistEpisodeModelOptions
    ]
    exclude = ['playlist', ]

    def make_hero_from_episode(self, request, queryset):
        """
            1) Takes every selected Episode
            2) Creates Hero Entry object with data from Episode
            3) Does in the 'index' Hero, but should be changable.
        """
        for e in queryset:
            he = HeroEntry()
            try:
                he.hero = Hero.objects.get(slug = 'index')
                he.title = e.title
                he.subtitle = unicode(e.program.name)+u' #'+unicode(e.number)
                he.text = e.short
                he.image = e.image
                he.url = e.get_absolute_url()
                he.button_text = _(u'Zobacz odcinek')
                he.save()
            except Hero.DoesNotExist:
                self.message_user(request, u'Rotator główny (index) nie istnieje')
                return
        self.message_user(request, u'%s utworzonych wpisów rotatora' % queryset.count())
    make_hero_from_episode.short_decription = u'Wygeneruj wpis w rotatorze'

    def publish(self, request, queryset):
        """
            Activates chosen episodes
        """
        queryset.update(active = True)
        self.message_user(request, u'%s opublikowanych odcinków' % queryset.count())
    publish.short_decription = u'Publikuj odcinek'


class ProgramAdmin(admin.ModelAdmin):
    actions = ['migrate_to_playlist', ]

    def migrate_to_playlist(self, request, queryset):
        added_playlists = 0
        added_episodes = 0
        for program in queryset:
            playlist = Playlist.objects.create_from_program(program)
            added_playlists += 1
            added_episodes += playlist.episodes.count()

        from django.contrib import messages
        messages.success(request, 'Added {} playlists with {} episodes'.format(
            added_playlists,
            added_episodes
        ))

    migrate_to_playlist.short_description = 'Migrate episodes from Program to Playlist'


class HostAdmin(admin.ModelAdmin):
    pass


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', ]
    prepopulated_fields = {'slug': ('name',), }
    raw_id_fields = ('related_event',)
    autocomplete_lookup_fields = {
        'fk': ['related_event'],
    }

    inlines = [SortablePlaylistEpisodeModelOptions, ]


admin.site.register(Host, HostAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Playlist, PlaylistAdmin)
