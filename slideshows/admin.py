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

class SlideAdmin(admin.ModelAdmin):
    ordering = ('priority',)
    search_fields = ('title', 'content')
    list_filter = ('created',)
    list_display = (admin_image, 'title', 'priority', 'created')

admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Slide, SlideAdmin)
