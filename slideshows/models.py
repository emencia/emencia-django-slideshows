# -*- coding: utf-8 -*-
"""
Models
"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from filebrowser.fields import FileBrowseField
from django.utils.encoding import python_2_unicode_compatible


# Try to find a django app for the CKeditor, else fallback on TextField
try:
    from djangocms_text_ckeditor.fields import HTMLField
except ImportError:
    # djangocms_text_ckeditor is not installed
    try:
        from ckeditor.fields import RichTextField
    except ImportError:
        # None of ckeditor app is installed
        CkeditorField = models.TextField
    else:
        CkeditorField = RichTextField
else:
    CkeditorField = HTMLField

PUBLISHED_CHOICES = (
    (True, _('Published')),
    (False, _('Unpublished')),
)

DEFAULT_SLIDESHOWS_TEMPLATE = getattr(settings, 'DEFAULT_SLIDESHOWS_TEMPLATE', '')
DEFAULT_SLIDESHOWS_CONFIG = getattr(settings, 'DEFAULT_SLIDESHOWS_CONFIG', '')
DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE = getattr(settings, 'DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE', '')


@python_2_unicode_compatible
class Slideshow(models.Model):
    """
    Slideshow that contains slides
    """
    created = models.DateTimeField(_('created'), blank=True, editable=False)
    title = models.CharField(_('title'), blank=False, max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=75)
    template = models.CharField(_('content template'),
                                choices=settings.SLIDESHOWS_TEMPLATES,
                                default=DEFAULT_SLIDESHOWS_TEMPLATE,
                                max_length=100, blank=False)
    config = models.CharField(
        _('config template'),
        choices=settings.SLIDESHOWS_CONFIGS,
        default=DEFAULT_SLIDESHOWS_CONFIG,
        max_length=100,
        blank=True,
        help_text=_('Config file to configure and initialize slideshow'),
    )
    transition_time = models.IntegerField(
        _('transition time'),
        default=0,
        null=True,
        blank=True,
        help_text=_('Sets the amount of time in milliseconds before '
                    'transitioning a slide. Set 0 to use default value.'),
    )

    def __str__(self):
        return self.title

    def get_published_slides(self):
        return self.slide_set.filter(publish=True)

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = timezone.now()

        super(Slideshow, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Slide(models.Model):
    """
    Slide item
    """
    slideshow = models.ForeignKey(
        Slideshow,
        verbose_name=_('slideshow'),
        blank=False,
    )
    created = models.DateTimeField(
        _('created'),
        blank=True,
        editable=False,
    )
    title = models.CharField(
        _('title'),
        blank=False,
        max_length=255,
    )
    priority = models.IntegerField(
        _('display priority'),
        default=100,
        help_text=_('Priority display value'),
    )
    publish = models.BooleanField(
        _('published'),
        choices=PUBLISHED_CHOICES,
        default=True,
        help_text=_('Unpublished slide will not be displayed in its slideshow'),
    )
    content = CkeditorField(
        _("content"),
        blank=True,
    )
    image = FileBrowseField(
        _('image'),
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    url = models.CharField(
        _('url'),
        blank=True,
        max_length=255,
        help_text=_('An URL that can be used in the template for this entry'),
    )
    open_blank = models.BooleanField(
        _('open new window'),
        default=False,
        help_text=_('If checked the link will be open in a new window'),
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # First create
        if not self.created:
            self.created = timezone.now()

        super(Slide, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")
        ordering = ('priority',)
