# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-03 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0010_auto_20180603_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='program.Program'),
        ),
    ]