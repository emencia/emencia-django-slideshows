# -*- coding: utf-8 -*-
"""
Models
"""
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from djangocms_text_ckeditor.fields import HTMLField

from .utils import content_file_name

IMAGE_FILE_UPLOADTO = lambda x,y: content_file_name('slideshows/slides/%Y/%m/%d', x, y)

PUBLISHED_CHOICES = (
    (True, _('Published')),
    (False, _('Unpublished')),
)

DEFAULT_SLIDESHOWS_TEMPLATE = getattr(settings, 'DEFAULT_SLIDESHOWS_TEMPLATE', '')
DEFAULT_SLIDESHOWS_CONFIG = getattr(settings, 'DEFAULT_SLIDESHOWS_CONFIG', '')
DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE = getattr(settings, 'DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE', '')


class Slideshow(models.Model):
    """
    Slideshow that contains slides
    """
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=75)
    template = models.CharField(_('content template'), choices=settings.SLIDESHOWS_TEMPLATES, default=DEFAULT_SLIDESHOWS_TEMPLATE, max_length=100, blank=False)
    config = models.CharField(_('config template'), choices=settings.SLIDESHOWS_CONFIGS, default=DEFAULT_SLIDESHOWS_CONFIG, max_length=100, blank=True, help_text=_('The Javascript config file to use to configure and initialize the slideshow'))
    timer_speed = models.IntegerField(_('timer speed'), default=0, null=True, blank=True, help_text=_('Sets the amount of time in milliseconds before transitioning a slide. Set 0 to use default value.'))


    def __unicode__(self):
        return self.title

    def get_published_slides(self):
        return self.slide_set.filter(publish=True)

    def count_published_slides(self):
        return self.get_published_slides().count()
    count_published_slides.short_description = _('Published slides')

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = datetime.datetime.now()

        super(Slideshow, self).save(*args, **kwargs)


class Slide(models.Model):
    """
    Slide item
    """
    slideshow = models.ForeignKey(Slideshow, verbose_name=_('slideshow'), blank=False)
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)
    priority = models.IntegerField(_('display priority'), default=100, help_text=_('Priority display value'))
    publish = models.BooleanField(_('published'), choices=PUBLISHED_CHOICES, default=True, help_text=_('Unpublished slide will not be displayed in its slideshow'))
    content = HTMLField(_("content"), blank=True)
    image = models.ImageField(_('image'), upload_to=IMAGE_FILE_UPLOADTO, max_length=255, blank=True)
    url = models.CharField(_('url'), blank=True, max_length=255, help_text=_('An URL that can be used in the template for this entry'))
    url_new_window = models.BooleanField(_('new window'), default=False, help_text=_('If checked the link will be open in a new window'))

    def __unicode__(self):
        return self.title

    @property
    def get_file(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def clean(self):
        if not self.get_file:
            raise ValidationError(_('Please fill an image'))

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = datetime.datetime.now()

        super(Slide, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")
        ordering = ('priority',)

try:
    from cms.models import CMSPlugin
except ImportError:
    pass
else:
    class SlideshowPlugin(CMSPlugin):
        slideshow = models.ForeignKey('slideshows.Slideshow')
        template = models.CharField(_('content template'), choices=settings.SLIDESHOWS_TEMPLATES, default=DEFAULT_SLIDESHOWS_TEMPLATE, max_length=100, blank=False)

        def __unicode__(self):
            return self.slideshow.title

    class SlideshowRandomImagePlugin(CMSPlugin):
        slideshow = models.ForeignKey('slideshows.Slideshow')
        template = models.CharField(_('content template'), choices=settings.SLIDESHOWS_RANDOM_SLIDE_TEMPLATES, default=DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE, max_length=100, blank=False)

        def __unicode__(self):
            return self.slideshow.title
