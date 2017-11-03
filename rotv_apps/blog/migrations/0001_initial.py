# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-22 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import tagging.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nazwa')),
                ('slug', models.SlugField(unique=True, verbose_name='Adres/Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategorie',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tytu\u0142')),
                ('slug', models.SlugField(unique=True, verbose_name='Adres/Slug')),
                ('text', models.TextField(verbose_name='Tre\u015b\u0107')),
                ('new_tags', tagging.fields.TagField(blank=True, max_length=255, null=True, verbose_name='Tagi')),
                ('posted', models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Zmieniono')),
                ('active', models.BooleanField(default=False, help_text='Zaznacz, je\u017celi tekst jest gotowy do publikacji (nie notka)', verbose_name='Aktywny')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Czas publikacji')),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'blog-images', verbose_name='Obraz szeroki')),
                ('image_right', models.ImageField(blank=True, null=True, upload_to=b'blog-images', verbose_name='Obraz w\u0105ski/p\u0142ywaj\u0105cy')),
                ('image_float', models.CharField(blank=True, choices=[(b'alignleft', 'Do lewej'), (b'alignright', 'Do prawej'), (b'aligncenter', 'Do \u015brodka')], default=b'alignleft', max_length=15, null=True, verbose_name='Wyr\xf3wnanie obrazka')),
                ('categories', models.ManyToManyField(to='blog.Category', verbose_name='Kategorie')),
            ],
            options={
                'ordering': ['-publish_time', '-posted', '-pk'],
                'verbose_name': 'Wpis',
                'verbose_name_plural': 'Wpisy',
            },
        ),
    ]