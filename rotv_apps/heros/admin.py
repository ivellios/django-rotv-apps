# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin

from models import Hero, HeroEntry


class HeroEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'publish_time', 'added', 'modified', 'sort', 'hero']
    list_filter = ['hero']
    search_fields = ['title', 'subtitle', 'text', ]
    raw_id_fields = ('hero',)
    autocomplete_lookup_fields = {
        'fk': ['hero', 'hero.title', 'hero.slug'],
    }

    def reset_sorting(self, request, queryset):
        queryset.update(sort = 100)


class HeroEntryInline(admin.TabularInline):
    model = HeroEntry
    fields = ['title', 'subtitle', 'is_active', 'url']


class HeroAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HeroEntryInline, ]


admin.site.register(HeroEntry, HeroEntryAdmin)
admin.site.register(Hero, HeroAdmin)
