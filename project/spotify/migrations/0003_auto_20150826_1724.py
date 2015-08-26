# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spotify', '0002_auto_20150826_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGenre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('proportion', models.FloatField()),
                ('genre', models.ForeignKey(to='spotify.Genre')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='genre',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='spotify.UserGenre'),
        ),
    ]
