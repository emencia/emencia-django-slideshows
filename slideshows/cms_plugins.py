from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from slideshows.models import SlideshowPlugin as SlideshowPluginModel

class SlideshowPlugin(CMSPluginBase):
    model = SlideshowPluginModel # Model where data about this plugin is saved
    name = _("Slideshow Plugin",) # Name of the plugin
    render_template = "slideshows/default.html" # template to render the plugin with
    
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
        js_config = self.get_config_render(context, instance.slideshow)
        
        context.update({
            'instance': instance,
            'slideshow_js_config': mark_safe(js_config),
            'slideshow_instance': instance.slideshow,
            'slideshow_slides': instance.slideshow.get_published_slides(),
        })
        return context

plugin_pool.register_plugin(SlideshowPlugin) # register the plugin