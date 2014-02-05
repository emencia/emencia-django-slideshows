import random

from django.db.models import Count
from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from slideshows.models import SlideshowPlugin as SlideshowPluginModel

class SlideshowPluginBase(CMSPluginBase):
    module = 'Slideshow'

class SlideshowPlugin(SlideshowPluginBase):
    """
    Standard plugin to embed a slideshow
    """
    model = SlideshowPluginModel # Model where data about this plugin is saved
    name = _("Slides show",) # Name of the plugin
    render_template = "slideshows/slides_show/default.html" # template to render the plugin with
    
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
        if not instance.config:
            return ""
        
        t = template.loader.get_template(instance.config)
        context.update({
            'slideshow_instance': instance,
            'slideshow_slides': instance.get_published_slides(),
        })
        content = t.render(template.Context(context))
        
        return content

    def render(self, context, instance, placeholder):
        self.render_template = instance.slideshow.template
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
    model = SlideshowPluginModel # Model where data about this plugin is saved
    name = _("Random single slide",) # Name of the plugin
    render_template = "slideshows/random_slide/default.html" # template to render the plugin with
    
    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'slideshow_instance': instance.slideshow,
            'slideshow_slide': self.get_random_slide(instance.slideshow.get_published_slides()),
        })
        return context
    
    def get_random_slide(self, queryset):
        """
        Efficient random select, "order_by('?')" is knowed as slow/painful for some database
        """
        count = queryset.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return queryset.all()[random_index]

# Register plugins
plugin_pool.register_plugin(SlideshowPlugin)
plugin_pool.register_plugin(RandomImagePlugin)