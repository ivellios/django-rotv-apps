from django.contrib import admin
from .models import ShortenedURL


class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ['url', 'slug', 'get_shortened_url',
                    'expires', 'created', 'modified', 'created_by', 'modified_by']
    search_fields = ['url', 'slug', ]
    list_filter = ['expires', 'created', 'modified']
    readonly_fields = ('created_by', 'modified_by')

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance


admin.site.register(ShortenedURL, ShortenedURLAdmin)
