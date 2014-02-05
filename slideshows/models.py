# -*- coding: utf-8 -*-
"""
Modèles de données
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

class Slideshow(models.Model):
    """
    Slideshow that contains slides
    """
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=75)
    template = models.CharField(_('content template'), choices=settings.SLIDESHOWS_TEMPLATES, default=settings.SLIDESHOWS_TEMPLATES[0][0], max_length=100, blank=False)
    config = models.CharField(_('config template'), choices=settings.SLIDESHOWS_CONFIGS, default="", max_length=100, blank=True, help_text=_('The Javascript config file to use to configure and initialize the slideshow'))

    def __unicode__(self):
        return self.title
    
    def get_published_slides(self):
        return self.slide_set.filter(publish=True)

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

        def __unicode__(self):
            return self.slideshow.title

    class SlideshowRandomImagePlugin(CMSPlugin):
        slideshow = models.ForeignKey('slideshows.Slideshow')

        def __unicode__(self):
            return self.slideshow.title
