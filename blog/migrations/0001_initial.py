# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-31 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Baslik Bilgisi Burada Girilir.', max_length=100, null=True, verbose_name='Baslik Giriniz.')),
                ('icerik', models.TextField(max_length=1000, null=True, verbose_name='İcerik Giriniz')),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]