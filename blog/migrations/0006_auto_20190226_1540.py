# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-26 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_kategoriler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='kategoriler',
            field=models.ManyToManyField(null=True, related_name='blog', to='blog.Kategori'),
        ),
    ]