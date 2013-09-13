.. _django-cms: http://www.django-cms.org/
.. _South: http://south.readthedocs.org/en/latest/
.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail
.. _djangocms_text_ckeditor: https://github.com/divio/djangocms-text-ckeditor
.. _Orbit Foundation 3: http://foundation.zurb.com/old-docs/f3/orbit.php

A Django application to make slideshows.

Very simple, you can have multiple Slideshows, and each of them have their own slides. Slides can be ordered and they contains a title, an optional content text, an optional URL and an image.

Slideshows can use custom templates and can use a custom config templates. Config templates are used to contains some Javascript to configure/initialize your slideshow with your slider library. By default, a Slideshow item have no config template, this is optional.

There is no dedicated view to display them, only a template tag to use in your templates or a plugin to use with `django-cms`_.

Although it has been developed for `Orbit Foundation 3`_ slider, it does not contains any assets to integrate it in your site, this is at your responsability to integrate it (add your assets where your need, customise the template, etc..).

Require
=======

* `sorl-thumbnail`_;
* `djangocms_text_ckeditor`_ to easier content edit;

Optional
********

`South`_ migration is supported. This is not required, but strongly recommended for future updates.

Install
=======

Add it to your installed apps in the settings : ::

    INSTALLED_APPS = (
        ...
        'slideshows',
        ...
    )

Then add the following settings : ::

    # Available templates to display a slideshow
    SLIDESHOWS_TEMPLATES = (
        ("slideshows/default.html", "Default template"),
    )

    # Available config file to initialize your slideshow Javascript stuff
    SLIDESHOWS_CONFIGS = (
        ("slideshows/configs/default.html", "Default config"),
    )

You can fill entries with your custom templates if needed.

And finally add the new models to your database :

    ./manage.py syncdb

If DjangoCMS is installed (this should be as `djangocms_text_ckeditor`_ require it), a plugin will be available to use slideshows in your pages.

Update
======

If you have installed `South`_, after updating an existing install to a major new version you can automatically update your database :

    ./manage.py migrate slideshows

Usage
=====

Either with the template tag or the cms plugin, the process to build the HTML will be to generate the optional config HTML if any, then generate the content HTML (where the config HTML would be avalaible as a context variable).

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
    {% slideshow_render 'your-slug' 'slideshows/custom.html' 'slideshows/configs/custom.html' %}

(Use ``'None'`` as the second argument if you just want to override the config template).

Note that if you the given Slideshow slug does not exist, this will raise a Http404.

With the cms plugin
*******************

Just go to the pages admin, and use the plugin in a placeholder content. You will have to select a Slideshow that will be used in your page.

Note that plugin use only the content template and config template save on the Slideshow.

Templates
*********

Slideshow content templates will have the following context variables :

* slideshow_js_config : the generated config template if any, else an empty string;
* slideshow_instance : the Slideshow model instance;
* slideshow_slides : a queryset of published slides for the Slideshow instance;

Slideshow config templates will have the following context variables :

* slideshow_instance : the Slideshow model instance;
* slideshow_slides : a queryset of published slides for the Slideshow instance;

This available for the template tag and the cms plugin.
