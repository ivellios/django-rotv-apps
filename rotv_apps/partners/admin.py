# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Partner, MediaPatron, MediaPatronage, NormalMediaPatronage, Colaborator


def activate_patronage(modeladmin, request, queryset):
    queryset.update(active=True)


activate_patronage.short_description = u'Oznacz wybrane wydarzenia jako aktywne'


class MediaPatronageAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'spot',
                    'start', 'end', 'active', 'activated',
                    'contact_email',
                    'created', 'modified']
    

class NormalMediaPatronageAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'active']


admin.site.register(MediaPatronage, MediaPatronageAdmin)
admin.site.register(NormalMediaPatronage, NormalMediaPatronageAdmin)

admin.site.register(Partner)
admin.site.register(MediaPatron)
admin.site.register(Colaborator)

