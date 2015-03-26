"""
Admin for sliders
"""
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

class SlideInline(admin.StackedInline):
    model = Slide

class SlideshowAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title',)
    list_filter = ('created',)
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title', 'count_published_slides', 'created')
    fieldsets = (
        (None, {
            'classes': ['wide',],
            'fields': ('title','slug','transition_time'),
        }),
        (_('Templates'), {
            'classes': ['wide',],
            'fields': ('template', 'config')
        }),
    )
    inlines = [
        SlideInline,
    ]

class SlideAdmin(admin.ModelAdmin):
    ordering = ('slideshow__slug', 'priority',)
    search_fields = ('title', 'content')
    list_filter = ('created', 'slideshow', 'publish')
    list_display = (admin_image, 'title', 'slideshow', 'priority', 'publish', 'hide_title', 'created')
    list_editable = ('priority', 'publish', 'hide_title',)
    fieldsets = (
        (None, {
            'fields': ('slideshow',),
        }),
        (None, {
            'fields': ('title', 'hide_title', 'priority', 'publish')
        }),
        (None, {
            'fields': ('image',)
        }),
        (None, {
            'fields': ('url', 'open_blank')
        }),
        (None, {
            'fields': ('content',),
        }),
    )

admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Slide, SlideAdmin)
