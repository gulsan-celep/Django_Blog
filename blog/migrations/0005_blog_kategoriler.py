# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-26 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_kategori'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(null=True, to='blog.Kategori'),
        ),
    ]
