# -*- coding: utf-8 -*-
"""
Views
"""
import random

from django.db.models import Count
from django import template
from django.views.generic.detail import DetailView
from django.utils.safestring import mark_safe

from slideshows.models import Slideshow, DEFAULT_SLIDESHOWS_TEMPLATE, DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE


class SlideshowMixin(object):
    """
    Mixin to share some Slideshow display logic
    """
    def get_template_names(self):
        return [self.object.template or DEFAULT_SLIDESHOWS_TEMPLATE]

    def get_config_render(self, context, instance):
        """
        Render the slideshow Javascript config using the defined template.

        If the Slideshow instance has an empty "config" attribute this
        will return an empty string.

        :type instance: ``slideshows.models.Slideshow`` instance object
        :param instance: A slideshow instance

        :type context: object ``django.template.Context``
        :param context: Context object

        :rtype: string
        :return: HTML for the slideshow's config
        """
        if not instance.config:
            return ""

        t = template.loader.get_template(instance.config)
        context['slideshow_instance'] = instance
        content = t.render(template.Context(context))

        return content

    def get_random_slide(self, queryset):
        """
        Efficient random select, because "order_by('?')" is known to be
        slow/painful for some database

        :type queryset: Queryset
        :param queryset: Slideshow queryset to start from

        :rtype: ``slideshows.models.Slideshow`` instance object
        :return: A random slideshow getted from the given queryset
        """
        count = queryset.aggregate(count=Count('id'))['count']
        if count == 0:
            return []
        random_index = random.randint(0, count - 1)
        return queryset.all()[random_index]


class SlideshowView(SlideshowMixin, DetailView):
    model = Slideshow

    def get_context_data(self, **kwargs):
        context = super(SlideshowView, self).get_context_data(**kwargs)
        context['slideshow_slides'] = self.object.get_published_slides()
        context['slideshow_js_config'] = mark_safe(self.get_config_render(context, self.object))
        return context


class RandomImageView(SlideshowMixin, DetailView):
    model = Slideshow

    def get_template_names(self):
        return [DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE]

    def get_context_data(self, **kwargs):
        context = super(RandomImageView, self).get_context_data(**kwargs)
        context['slideshow_slide'] = self.get_random_slide(self.object.get_published_slides())
        return context
