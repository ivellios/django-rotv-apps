# -*- coding: utf-8 -*-

from django.contrib import admin

from models import *
from django.conf import settings


class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted', 'publish_time', 'active', 'modified', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['categories']
    search_fields = ['title']
    raw_id_fields = ('categories',)
    autocomplete_lookup_fields = {
        'm2m': ['categories'],
    }

    class Media:
        js = (settings.STATIC_URL+'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              settings.STATIC_URL+'filebrowser/js/TinyMCEAdmin.js',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
