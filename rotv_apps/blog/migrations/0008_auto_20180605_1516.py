# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-05 13:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_entry_related_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='related_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_entries', to='partners.MediaPatronage'),
        ),
    ]
