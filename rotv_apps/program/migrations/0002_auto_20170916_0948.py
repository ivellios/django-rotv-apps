# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-16 07:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together=set([('number', 'program')]),
        ),
    ]
