# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-18 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('heros', '0003_auto_20170918_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroentry',
            name='publish_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publikacja'),
        ),
    ]
