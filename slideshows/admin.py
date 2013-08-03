"""Admin for sliders"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.shortcuts import get_thumbnail

from .models import Slideshow, Slide

def admin_image(obj):
    if obj.image:
        try:
            thumbnail = get_thumbnail(obj.image, '75x75')
        except:
            return _('Invalid image for %s') % unicode(obj)
        url = thumbnail.url
        return '<img src="%s" alt="%s" />' % (url, unicode(obj))
    else:
        return _('No image for %s') % unicode(obj)
admin_image.short_description = _('image')
admin_image.allow_tags = True

class SlideshowAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('created',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title', 'created')

class SlideAdmin(admin.ModelAdmin):
    ordering = ('priority',)
    search_fields = ('title', 'content')
    list_filter = ('created', 'slideshow')
    list_display = (admin_image, 'title', 'slideshow', 'priority', 'publish', 'created')
    list_editable = ('priority', 'publish',)
    fieldsets = (
        (None, {
            'fields': ('slideshow',),
        }),
        (None, {
            'fields': ('title', 'priority', 'publish')
        }),
        (None, {
            'fields': ('image',)
        }),
        (None, {
            'fields': ('content',),
        }),
    )

admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Slide, SlideAdmin)
