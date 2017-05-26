"""
Admin for sliders
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from filebrowser.settings import ADMIN_THUMBNAIL

from .models import Slideshow, Slide


def slide_image_thumbnail(obj):
    if obj.image and obj.image.filetype == "Image":
        return '<img src="%s" />' % obj.image.version_generate(ADMIN_THUMBNAIL).url
    else:
        return _('No image for %s') % force_text(obj)


slide_image_thumbnail.short_description = _('image')
slide_image_thumbnail.allow_tags = True


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
            'classes': ['wide'],
            'fields': ('title', 'slug', 'transition_time'),
        }),
        (_('Templates'), {
            'classes': ['wide'],
            'fields': ('template', 'config')
        }),
    )

    def count_published_slides(self, instance):
        return instance.get_published_slides().count()
    count_published_slides.short_description = _('Published slides')

    inlines = [
        SlideInline,
    ]


class SlideAdmin(admin.ModelAdmin):
    ordering = ('slideshow__slug', 'priority',)
    search_fields = ('title', 'content')
    list_filter = ('created', 'slideshow', 'publish')
    list_display = (slide_image_thumbnail, 'title', 'slideshow', 'priority', 'publish', 'created')
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
            'fields': ('url', 'open_blank')
        }),
        (None, {
            'fields': ('content',),
        }),
    )


admin.site.register(Slideshow, SlideshowAdmin)
admin.site.register(Slide, SlideAdmin)
