.. _DjangoCMS: http://www.django-cms.org/
.. _South: http://south.readthedocs.org/en/latest/
.. _django-filebrowser: https://github.com/sehmaschine/django-filebrowser
.. _django-filebrowser-no-grappelli: https://github.com/smacker/django-filebrowser-no-grappelli
.. _djangocms_text_ckeditor: https://github.com/divio/djangocms-text-ckeditor

Introduction
============

Very simple, you can have multiple Slideshows and each of them have their own slides. Slides can be ordered and they contains a title, an optional content text, an optional URL and an optional image.

Slideshows can use custom templates and custom config templates. Config templates are used to contains some Javascript to configure/initialize your slideshow with your slider library. But by default a Slideshow item have no config template, this is optional.

It does not contains any assets to integrate it in your site, this is at your responsability to integrate it (choose and install your slider library, add your assets where you need, customise the template, etc..).

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/emencia-django-slideshows>`_;
* Clone it on his `Github repository <https://github.com/emencia/emencia-django-slideshows>`_;

Require
=======

* Django >= 1.6 (Django <= 1.5 support has been dropped);
* `django-filebrowser`_ >= 3.5.6 or `django-filebrowser-no-grappelli`_ >= 3.5.6 (depends if you use django-grapelli or not);
* `DjangoCMS`_ >= 3.0;
* `djangocms_text_ckeditor`_ to easier content edit;

Optional
********

* `South`_ migration is supported. This is not required, but strongly recommended for future updates;

Install
=======

Add it to your installed apps in the settings : ::

    INSTALLED_APPS = (
        ...
        'slideshows',
        'filebrowser',
        ...
    )

Then add the following settings : ::

    # Available templates to display a slideshow
    SLIDESHOWS_TEMPLATES = (
        ("slideshows/slides_show/default.html", "Default template"),
    )

    # Available config file to initialize your slideshow Javascript stuff
    SLIDESHOWS_CONFIGS = (
        ("slideshows/slides_show/configs/default.html", "Default config"),
    )

    # Available templates for "random slide" mode
    SLIDESHOWS_RANDOM_SLIDE_TEMPLATES = (
        ("slideshows/random_slide/default.html", "Random image default"),
    )

    # Default templates to use in admin forms
    DEFAULT_SLIDESHOWS_TEMPLATE = SLIDESHOWS_TEMPLATES[0][0]
    DEFAULT_SLIDESHOWS_CONFIG = ""
    DEFAULT_SLIDESHOWS_RANDOM_SLIDE_TEMPLATE = SLIDESHOWS_RANDOM_SLIDE_TEMPLATES[0][0]

And some `django-filebrowser`_ settings (see its documentation for more details) : ::

    FILEBROWSER_VERSIONS_BASEDIR = '_uploads_versions'

    FILEBROWSER_MAX_UPLOAD_SIZE = 10*1024*1024 # 10 Mb

    FILEBROWSER_NORMALIZE_FILENAME = True

And if you want to use the views add this to your main ``urls.py`` : ::

    from django.conf.urls import url, patterns
    from filebrowser.sites import site as filebrowser_site

    urlpatterns = patterns('',
        ...
        url(r'^slideshows/', include('slideshows.urls', namespace='slideshows')),
        url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
        ...
    )

You can fill entries with your custom templates if needed.

And finally add the new models to your database : ::

    ./manage.py syncdb

If DjangoCMS is installed (this should be as `djangocms_text_ckeditor`_ require it), a plugin will be available to use slideshows in your pages.

Update
======

If you have installed `South`_, after updating an existing install to a major new version you can automatically update your database : ::

    ./manage.py migrate slideshows

Usage
=====

Either with the template tag or the `DjangoCMS`_ plugins, the process to build the HTML will be to generate the optional config HTML if any, then generate the content HTML (where the config HTML would be avalaible as a context variable).

The common way is to display a Slideshow with all its slides, this is called the **Slides show**. And there is an *extra mode* called **Random slide** which only a display a single slide take randomly from the published slides of a Slideshow.

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

With the DjangoCMS plugins
**************************

Just go to the pages admin, and use the plugin you want in a placeholder content. You will have to select a Slideshow that will be used in your page.

There is actually two plugins :

* **Slides show** : the default one to display your slides in a slideshow, it use the template defined in the slideshow object (or the default template if empty);
* **Random slide** : to display only one random slide, it will never use the template defined in the slideshow object, instead it will use the template ``slideshows/random_slide/default.html``. And unlike the *Slides show* plugin it don't embed a javascript config template because this is not really useful for a simple slide;

Templates
.........

Slideshow content templates will have the following context variables :

* ``slideshow_js_config`` : the generated config template if any, else an empty string;
* ``slideshow_instance`` : the Slideshow model instance;
* ``slideshow_slides`` : a queryset of published slides for the Slideshow instance;

Slideshow config templates will have the following context variables :

* ``slideshow_instance`` : the Slideshow model instance;
* ``slideshow_slides`` : a queryset of published slides for the Slideshow instance;

This is available for the template tag and the cms plugin.

With the views
**************

Views use the defined template in Slideshow instance, there is no particular process to define.

* You can reach a slideshow view with an url like ``/slideshows/show_slides/SLUG/`` where ``SLUG`` is the defined slug on the Slideshow object;
* You can reach the random image mode for a slideshow view with an url like ``/slideshows/random_slide/SLUG/`` where ``SLUG`` is the defined slug on the Slideshow object;
