# Generated by Django 2.2 on 2020-06-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0006_auto_20180503_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborator',
            name='logo',
            field=models.ImageField(upload_to='logos/colaborator', verbose_name='Logotyp'),
        ),
        migrations.AlterField(
            model_name='mediapatron',
            name='logo',
            field=models.ImageField(upload_to='logos/patron', verbose_name='Logotyp'),
        ),
        migrations.AlterField(
            model_name='mediapatronage',
            name='banner_image',
            field=models.ImageField(blank=True, help_text='Szerokość sugerowana: 800px', null=True, upload_to='uploads/partners/banners', verbose_name='Baner wydarzenia'),
        ),
        migrations.AlterField(
            model_name='mediapatronage',
            name='cover_image',
            field=models.ImageField(blank=True, help_text='Szerokość sugerowana: 1000-1600px', null=True, upload_to='uploads/partners/covers', verbose_name='Szeroki obraz typu cover'),
        ),
        migrations.AlterField(
            model_name='mediapatronage',
            name='logo',
            field=models.ImageField(upload_to='logos/patronage', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='mediapatronage',
            name='small_image',
            field=models.ImageField(blank=True, help_text='Szerokość sugerowana: 300px', null=True, upload_to='uploads/partners/images', verbose_name='Mały obrazk'),
        ),
        migrations.AlterField(
            model_name='normalmediapatronage',
            name='logo',
            field=models.ImageField(upload_to='logos/patronage', verbose_name='Logotyp'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.ImageField(upload_to='logos/partner', verbose_name='Logotyp'),
        ),
    ]
