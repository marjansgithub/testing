# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-18 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20161218_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='Review_text',
        ),
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
