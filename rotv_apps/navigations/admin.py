# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Nav


class NavAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'parent', 'subnav_type', 'slug', ]
    search_fields = ['name', ]
    list_filter = ['parent', ]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Nav, NavAdmin)
