# Generated by Django 2.0.7 on 2019-03-11 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_blog_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Gönderiler'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='blog', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]