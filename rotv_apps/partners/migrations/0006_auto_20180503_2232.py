# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-03 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0005_auto_20171230_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediapatronage',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail kontaktowy organizatora'),
        ),
    ]