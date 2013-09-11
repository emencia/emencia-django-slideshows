# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


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
            ('content', self.gf('djangocms_text_ckeditor.fields.HTMLField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
        ))
        db.send_create_signal('slideshows', ['Slide'])

        # Adding model 'SlideshowPlugin'
        db.create_table('cmsplugin_slideshowplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plugins', to=orm['slideshows.Slideshow'])),
        ))
        db.send_create_signal('slideshows', ['SlideshowPlugin'])


    def backwards(self, orm):
        # Deleting model 'Slideshow'
        db.delete_table('slideshows_slideshow')

        # Deleting model 'Slide'
        db.delete_table('slideshows_slide')

        # Deleting model 'SlideshowPlugin'
        db.delete_table('cmsplugin_slideshowplugin')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
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
        'slideshows.slideshowplugin': {
            'Meta': {'object_name': 'SlideshowPlugin', 'db_table': "'cmsplugin_slideshowplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plugins'", 'to': "orm['slideshows.Slideshow']"})
        }
    }

    complete_apps = ['slideshows']