# -*- coding: utf-8 -*-
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
