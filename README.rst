A Django application to make slideshows.

Very simple, you can have multiple slideshow, and each of them have their own slides. Slides can contains a title, a content text and an image, and they can be ordered.

Actually there is no view to display them, only a template tag to use in your templates.

Although it has been developed for Orbit Foundation slider, it does not contains any assets to integrate it in your site, this is at your responsability to integrate it (add your assets where your need, customise the template, etc..).

Require
=======

* ``sorl-thumbnail``;
* ``django-tinymce`` to easier content edit;

Usage
=====

Create your slideshow from the admin then use it in your templates : ::
    
    {% load slideshows_tags %}
    ...
    {% slideshow_render slug='your-slug' %}
