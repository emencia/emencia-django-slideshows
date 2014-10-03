import random

from django.conf import settings
from django.db.models import Count
from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from slideshows.models import SlideshowPlugin as SlideshowPluginModel
from slideshows.models import SlideshowRandomImagePlugin as SlideshowRandomImagePluginModel
from slideshows.models import DEFAULT_SLIDESHOWS_TEMPLATE, DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE
from slideshows.views import SlideshowMixin

class SlideshowPluginBase(SlideshowMixin, CMSPluginBase):
    module = 'Slideshow'


class SlideshowPlugin(SlideshowPluginBase):
    """
    Standard plugin to embed a slideshow
    """
    model = SlideshowPluginModel
    name = _("Slides show",)
    render_template = DEFAULT_SLIDESHOWS_TEMPLATE

    def render(self, context, instance, placeholder):
        self.render_template = instance.template
        js_config = self.get_config_render(context, instance.slideshow)
        
        context.update({
            'instance': instance,
            'slideshow_js_config': mark_safe(js_config),
            'slideshow_instance': instance.slideshow,
            'slideshow_slides': instance.slideshow.get_published_slides(),
        })
        return context


class RandomImagePlugin(SlideshowPluginBase):
    """
    Plugin to embed a random image from a slideshow
    """
    model = SlideshowRandomImagePluginModel
    name = _("Random slide",)
    render_template = DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE
    
    def render(self, context, instance, placeholder):
        self.render_template = instance.template
        context.update({
            'instance': instance,
            'slideshow_instance': instance.slideshow,
            'slideshow_slide': self.get_random_slide(instance.slideshow.get_published_slides()),
        })
        return context


# Register plugins
plugin_pool.register_plugin(SlideshowPlugin)
plugin_pool.register_plugin(RandomImagePlugin)