"""Urls for emencia-django-socialaggregator"""
from django.conf.urls import url, patterns

from slideshows.views import SlideshowView, RandomImageView

urlpatterns = patterns('',
    url(r'^show_slides/(?P<slug>[-\w]+)/$', SlideshowView.as_view(), name='show_slides'),
    url(r'^random_slide/(?P<slug>[-\w]+)/$', RandomImageView.as_view(), name='random_slide'),
)
