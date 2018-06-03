# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-02 23:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tagging.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_slug_prepopulate'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together=set([]),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Description')),
                ('new_tags', tagging.fields.TagField(blank=True, max_length=255, null=True, verbose_name='Tags')),
            ],
        ),
        migrations.AlterField(
            model_name='episode',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='program',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
