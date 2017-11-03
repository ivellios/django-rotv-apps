# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Partner, MediaPatron, MediaPatronage, NormalMediaPatronage, Colaborator


class MediaPatronageAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'active']
    

class NormalMediaPatronageAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'active']

admin.site.register(MediaPatronage, MediaPatronageAdmin)
admin.site.register(NormalMediaPatronage, NormalMediaPatronageAdmin)

admin.site.register(Partner)
admin.site.register(MediaPatron)
admin.site.register(Colaborator)

