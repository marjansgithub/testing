# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_quote_quote_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_count',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
