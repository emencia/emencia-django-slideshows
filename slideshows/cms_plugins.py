from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from slideshows.models import SlideshowPlugin as SlideshowPluginModel

class SlideshowPlugin(CMSPluginBase):
    model = SlideshowPluginModel # Model where data about this plugin is saved
    name = _("Slideshow Plugin",) # Name of the plugin
    render_template = "slideshows/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(SlideshowPlugin) # register the plugin