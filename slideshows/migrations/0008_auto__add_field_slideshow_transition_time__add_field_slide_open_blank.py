# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Slideshow.transition_time'
        db.add_column(u'slideshows_slideshow', 'transition_time',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Slide.open_blank'
        db.add_column(u'slideshows_slide', 'open_blank',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Slideshow.transition_time'
        db.delete_column(u'slideshows_slideshow', 'transition_time')

        # Deleting field 'Slide.open_blank'
        db.delete_column(u'slideshows_slide', 'open_blank')


    models = {
        u'slideshows.slide': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'Slide'},
            'content': ('djangocms_text_ckeditor.fields.HTMLField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'open_blank': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slideshows.Slideshow']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url_new_window': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'slideshows.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'config': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '75'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'slideshows/slides_show/default.html'", 'max_length': '100'}),
            'timer_speed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transition_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
    }

    complete_apps = ['slideshows']