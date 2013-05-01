# -*- coding: utf-8 -*-
"""
Templates tags divers pour les documents
"""
from django import template
from django.utils.safestring import mark_safe

from src.slideshows.models import Slide

register = template.Library()

def slideshow_render(context, a, b, *args, **kwargs):
    """
    Simple template tag to render template for all slides from the given slideshow
    
    TODO: Cache the queryset 
    """
    slides = Slide.objects.filter(priority__gt=0).order_by('priority')
    return {'slides': slides}

register.inclusion_tag('slideshows/slideshow.html', takes_context=True)(show_slider)