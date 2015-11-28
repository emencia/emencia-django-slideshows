.. _DjangoCMS: http://www.django-cms.org/
.. _django-filebrowser: https://github.com/sehmaschine/django-filebrowser
.. _django-filebrowser-no-grappelli: https://github.com/smacker/django-filebrowser-no-grappelli
.. _djangocms_text_ckeditor: https://github.com/divio/djangocms-text-ckeditor
.. _django-ckeditor: https://github.com/shaunsephton/django-ckeditor
.. _cmsplugin-slideshows: https://github.com/emencia/cmsplugin-slideshows

Introduction
============

You can have **multiple Slideshows** and each of them **have their own slides**. Slides can be ordered and they contains a title, an optional content text, an optional URL and an optional image.

Slideshows can use custom templates and custom config templates. Config templates are used to contains some Javascript to configure/initialize your slideshow with your slider library. But by default a Slideshow item have no config template, this is optional.

It does not contains any assets to integrate it in your site, this is at your responsability to integrate it (choose and install your slider library, add your assets where you need, customize the template, etc..).

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/emencia-django-slideshows>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-slideshows>`_;

Require
=======

* Django >= 1.7;

  - Last release for *Django<1.7* is available on repository branch *django_1-6*;
  
* `django-filebrowser-no-grappelli`_ >= 3.5.6;

Optional
********

* `djangocms_text_ckeditor`_ >= 2.4.0 OR `django-ckeditor`_ >= 4.4.4 (see `Ckeditor`_ section);

Ckeditor
--------

A Ckeditor django app can be installed to use it for the ``Slide.content`` model attribute instead of the simple ``TextField``.

So **it is at your responsability** to manualy install (with pip, buildout, etc..) one of them if you need it. Once it's installed, you won't need to worry about this again.

Note that the default assumed app is `djangocms_text_ckeditor`_ and if not installed, `django-ckeditor`_ will be assumed. If you have installed both, `djangocms_text_ckeditor`_ will be used. If none of them is installed, the default Django field ``TextField`` will be used.

Choosing what app to install depends mostly from if you have allready installed DjangoCMS or not. If you have, you probably allready have its ckeditor app installed, so no need to install the other app because. If you don't have installed DjangoCMS, just install `django-ckeditor`_.

Finally you can add custom settings for CKeditor, see its documentation to see how to set them (you may have to go to official CKeditor documentation to know about available settings).

Install
=======

Add it to your installed apps in the settings : ::

    INSTALLED_APPS = (
        ...
        'slideshows',
        'filebrowser',
        ...
    )

If you have installed one of the django app for CKeditor, add it also to your ``settings.INSTALLED_APPS``.
    
Then add its settings : ::

    from porticus.settings import *

See the app ``settings.py`` file to see what settings you can override.

Also there is some settings you may see about `django-filebrowser-no-grappelli`_ (see its documentation for more details).

And add its views to your main ``urls.py`` : ::

    from django.conf.urls import url, patterns
    from filebrowser.sites import site as filebrowser_site

    urlpatterns = patterns('',
        ...
        url(r'^slideshows/', include('slideshows.urls', namespace='slideshows')),
        url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
        ...
    )

Finally install app models in your database using Django migrations: ::

    python manage.py migrate

Usage
=====

The process to build the HTML will be to generate the optional config HTML if any, then generate the content HTML.

The common way is to display a Slideshow with all slides, this is called the **Slides show**. And there is another mode called **Random slide** which only display a single slide taked randomly from a Slideshow published slides.

With the template tag
*********************

Create your slideshow from the admin, feed it with some slides, then use it in your templates : ::
    
    {% load slideshows_tags %}
    ...
    {% slideshow_render 'your-slug' %}

The first argument accept either a slug string or a Slideshow instance.

Also you can override the content template and the config template saved within the template tag : ::
    
    {% load slideshows_tags %}
    ...
    {% slideshow_render 'your-slug' 'slideshows/slides_show/custom.html' 'slideshows/slides_show/configs/custom.html' %}

(Use ``'None'`` as the second argument if you just want to override the config template).

Note that if the given Slideshow slug does not exist, this will raise a Http404.

With the views
**************

Views use the defined template in Slideshow instance, there is no particular process to define.

* You can reach a slideshow view with an url like ``/slideshows/show_slides/SLUG/`` where ``SLUG`` is the defined slug on the Slideshow object;
* You can reach the random image mode for a slideshow view with an url like ``/slideshows/random_slide/SLUG/`` where ``SLUG`` is the defined slug on the Slideshow object;

Within DjangoCMS pages
**********************

You can install an additional package to use your slideshows in pages placeholder contents. See `cmsplugin-slideshows`_.

Templates
*********

Slideshow content templates will have the following context variables :

* ``slideshow_js_config`` : the generated config template if any, else an empty string;
* ``slideshow_instance`` : the Slideshow model instance;
* ``slideshow_slides`` : a queryset of published slides for the Slideshow instance;

Slideshow config templates will have the following context variables :

* ``slideshow_instance`` : the Slideshow model instance;
* ``slideshow_slides`` : a queryset of published slides for the Slideshow instance;

This is available for the template tag and also the cms plugin.
