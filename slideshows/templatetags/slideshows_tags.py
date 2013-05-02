# -*- coding: utf-8 -*-
"""
Templates tags divers pour les documents
"""
from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404

from slideshows.models import Slideshow

register = template.Library()

def slideshow_render(context, **kwargs):
    """
    Simple template tag to render template for all slides from the given slideshow
    
    TODO: Cache the queryset 
    """
    slideshow = get_object_or_404(Slideshow, slug=kwargs['slug'])
    slides = slideshow.slide_set.filter(priority__gt=0).order_by('priority')
    return {'slides': slides}

register.inclusion_tag('slideshows/slideshow.html', takes_context=True)(slideshow_render)