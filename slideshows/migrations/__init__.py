def get_ckeditor_field_name():
    """
    Return python path to the rich text field to use
    
    1. If djangocms_text_ckeditor is installed it will be its HTMLField;
    2. Else if django-ckeditor is installed it will be used instead;
    3. Finally if none of them is installed, fallback to the simple Django TextField;
    """
    try:
        from djangocms_text_ckeditor.fields import HTMLField
    except ImportError:
        # djangocms_text_ckeditor is not installed
        try:
            from ckeditor.fields import RichTextField
        except ImportError:
            # None of ckeditor app is installed
            return 'django.db.models.fields.TextField'
        else:
            return 'ckeditor.fields.RichTextField'
    else:
        return 'djangocms_text_ckeditor.fields.HTMLField'
