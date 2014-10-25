# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """Moving template path strings 'slideshows/*' to 'slideshows/slides_show/*'"""
        old_path = 'slideshows/'
        new_path = 'slideshows/slides_show/'
        for slideshow in orm.Slideshow.objects.all():
            if not slideshow.template.startswith(new_path) and slideshow.template.startswith(old_path):
                slideshow.template = new_path + slideshow.template[len(old_path):]
                slideshow.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'slideshows.slide': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'Slide'},
            'content': ('djangocms_text_ckeditor.fields.HTMLField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slideshows.Slideshow']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'slideshows.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'config': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '75'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'slideshows/default.html'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
    }

    complete_apps = ['slideshows']
    symmetrical = True
