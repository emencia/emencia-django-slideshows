.. _django-cms: http://www.django-cms.org/
.. _south: http://south.readthedocs.org/en/latest/
.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail
.. _djangocms_text_ckeditor: https://github.com/divio/djangocms-text-ckeditor

A Django application to make slideshows.

Very simple, you can have multiple slideshow, and each of them have their own slides. Slides can contains a title, a content text and an image, and they can be ordered.

Actually there is no view to display them, only a template tag to use in your templates or a plugin to use with `django-cms`_.

Although it has been developed for Orbit Foundation slider, it does not contains any assets to integrate it in your site, this is at your responsability to integrate it (add your assets where your need, customise the template, etc..).

Require
=======

* `south`_;
* `sorl-thumbnail`_;
* `djangocms_text_ckeditor`_ to easier content edit;

Install
=======

Add it to your installed apps in the settings : ::

    INSTALLED_APPS = (
        ...
        'slideshows',
        ...
    )

Then add the new models to your database :

    ./manage.py syncdb

If DjangoCMS is installed (this should be as `djangocms_text_ckeditor`_ require it), a plugin will be available to use slideshows in your pages.

Update
======

If you update an existing install to a major new version, you will need to update your database :

    ./manage.py migrate slideshows

Usage
=====

Create your slideshow from the admin, feed it with some slides, then use it in your templates : ::
    
    {% load slideshows_tags %}
    ...
    {% slideshow_render slug='your-slug' %}

Or use it in your page as a content plugin with `django-cms`_.
