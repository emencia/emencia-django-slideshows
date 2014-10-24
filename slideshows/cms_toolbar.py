"""Toolbar extensions for CMS"""
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class SlideshowToolbar(CMSToolbar):

    def populate(self):
        slideshows_menu = self.toolbar.get_or_create_menu(
            'slideshows-menu', _('Slideshows'))

        url = reverse('admin:slideshows_slideshow_add')
        slideshows_menu.add_sideframe_item(_('New slideshow'), url=url)

        url = reverse('admin:slideshows_slide_add')
        slideshows_menu.add_sideframe_item(_('New ressource'), url=url)

        slideshows_menu.add_break()

        url = reverse('admin:slideshows_slideshow_changelist')
        slideshows_menu.add_sideframe_item(_('Slideshows list'), url=url)

        url = reverse('admin:slideshows_slide_changelist')
        slideshows_menu.add_sideframe_item(_('Slides list'), url=url)


toolbar_pool.register(SlideshowToolbar)
