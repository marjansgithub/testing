# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_user_user_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
