# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-26 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190226_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]
