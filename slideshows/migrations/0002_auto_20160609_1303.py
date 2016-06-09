# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='alt',
            field=models.CharField(max_length=255, verbose_name='alt', blank=True),
        ),
    ]
