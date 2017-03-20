# -*- coding: utf-8 -*-
"""
Template tags
"""
from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.utils.six import string_types

from slideshows.models import Slideshow

register = template.Library()


class SlideshowFragment(template.Node):
    """
    Get a slideshow HTML fragment
    """
    def __init__(self, slideshow_slug_varname, template_varname=None, config_varname=None):
        """
        :type insert_instance_varname: string or object ``django.db.models.Model``
        :param insert_instance_varname: Instance variable name or a string slug

        :type template_varname: string
        :param template_varname: custom template path to use instead of the one from the instance

        :type config_varname: string
        :param config_varname: custom config path to use instead of the one from the instance
        """
        self.slideshow_slug_varname = template.Variable(slideshow_slug_varname)
        self.template_varname = self.config_varname = self.custom_template = self.custom_config = None
        if template_varname:
            self.template_varname = template.Variable(template_varname)
        if config_varname:
            self.config_varname = template.Variable(config_varname)

    def render(self, context):
        """
        :type context: object ``django.template.Context``
        :param context: Context tag object

        :rtype: string
        :return: the HTML for the slideshow
        """
        # Default assume this is directly an instance
        slideshow_instance = self.slideshow_slug_varname.resolve(context)
        if self.template_varname:
            self.custom_template = self.template_varname.resolve(context)
        if self.config_varname:
            self.custom_config = self.config_varname.resolve(context)
        # Assume this is a slug (else will be used at an instance)
        if isinstance(slideshow_instance, string_types):
            slideshow_instance = get_object_or_404(Slideshow, slug=slideshow_instance)

        return mark_safe(self.get_content_render(context, slideshow_instance))

    def get_config_render(self, context, instance):
        """
        Render the slideshow Javascript config

        :type instance: ``slideshows.models.Slideshow`` instance object
        :param instance: A slideshow instance

        :type context: object ``django.template.Context``
        :param context: Context object

        :rtype: string
        :return: config HTML for the slideshow
        """
        used_config = self.custom_config or instance.config
        if not used_config:
            return ""

        t = template.loader.get_template(used_config)
        context.update({
            'slideshow_instance': instance,
            'slideshow_slides': instance.get_published_slides(),
        })
        content = t.render(template.Context(context))

        return content

    def get_content_render(self, context, instance):
        """
        Render the slideshow HTML content with its Javascript config

        :type instance: ``slideshows.models.Slideshow`` instance object
        :param instance: A slideshow instance

        :type context: object ``django.template.Context``
        :param context: Context object

        :rtype: string
        :return: the HTML for the slideshow
        """
        js_config = self.get_config_render(context, instance)

        used_template = self.custom_template or instance.template

        t = template.loader.get_template(used_template)
        context.update({
            'slideshow_js_config': mark_safe(js_config),
            'slideshow_instance': instance,
            'slideshow_slides': instance.get_published_slides(),
        })
        content = t.render(template.Context(context))

        return content


@register.tag(name="slideshow_render")
def do_slideshow_render(parser, token):
    """
    Display a slideshow HTML fragment

    Usage : ::

        {% slideshow_render [Slideshow SLUG or INSTANCE] [optional template overwrite] [optional config overwrite] %}
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError("You need to specify at less a \"Slideshow\" SLUG or INSTANCE")
    else:
        return SlideshowFragment(*args[1:])


do_slideshow_render.is_safe = True
