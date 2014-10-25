# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from __init__ import get_ckeditor_field_name

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Slideshow'
        db.create_table('slideshows_slideshow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('slideshows', ['Slideshow'])

        # Adding model 'Slide'
        db.create_table('slideshows_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['slideshows.Slideshow'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf(get_ckeditor_field_name())()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
        ))
        db.send_create_signal('slideshows', ['Slide'])


    def backwards(self, orm):
        # Deleting model 'Slideshow'
        db.delete_table('slideshows_slideshow')

        # Deleting model 'Slide'
        db.delete_table('slideshows_slide')


    models = {
        'slideshows.slide': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'Slide'},
            'content': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['slideshows.Slideshow']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'slideshows.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '75'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
    }

    complete_apps = ['slideshows']