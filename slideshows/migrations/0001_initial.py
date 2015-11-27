# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('priority', models.IntegerField(default=100, help_text='Priority display value', verbose_name='display priority')),
                ('publish', models.BooleanField(default=True, help_text='Unpublished slide will not be displayed in its slideshow', verbose_name='published', choices=[(True, 'Published'), (False, 'Unpublished')])),
                ('content', djangocms_text_ckeditor.fields.HTMLField(verbose_name='content', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(default=None, max_length=255, null=True, verbose_name='image', blank=True)),
                ('url', models.CharField(help_text='An URL that can be used in the template for this entry', max_length=255, verbose_name='url', blank=True)),
                ('open_blank', models.BooleanField(default=False, help_text='If checked the link will be open in a new window', verbose_name='open new window')),
            ],
            options={
                'ordering': ('priority',),
                'verbose_name': 'Slide',
                'verbose_name_plural': 'Slides',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(unique=True, max_length=75, verbose_name='slug')),
                ('template', models.CharField(default=b'slideshows/slides_show/default.html', max_length=100, verbose_name='content template', choices=[(b'slideshows/slides_show/default.html', b'Slider default'), (b'slideshows/slides_show/royalslider.html', b'Royal slider')])),
                ('config', models.CharField(default=b'', choices=[(b'slideshows/slides_show/configs/default.html', b'Slider default')], max_length=100, blank=True, help_text='The Javascript config file to use to configure and initialize the slideshow', verbose_name='config template')),
                ('transition_time', models.IntegerField(default=0, help_text='Sets the amount of time in milliseconds before transitioning a slide. Set 0 to use default value.', null=True, verbose_name='transition time', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='slide',
            name='slideshow',
            field=models.ForeignKey(verbose_name='slideshow', to='slideshows.Slideshow'),
            preserve_default=True,
        ),
    ]
