# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-02 23:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.deletion
import tagging.fields
import tinymce.models

class Migration(migrations.Migration):

    dependencies = [
        ('program', '0007_auto_20180603_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numer odcinka'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='program.Program'),
        ),
    ]
