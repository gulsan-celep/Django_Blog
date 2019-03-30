# Generated by Django 2.0.7 on 2019-03-07 13:52

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20190307_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='unique_id',
            field=models.CharField(editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='default/default-photo.jpg', help_text='Kapak Fotoğrafı Yükleyiniz', null=True, upload_to=blog.models.upload_to, verbose_name='Resim'),
        ),
    ]
