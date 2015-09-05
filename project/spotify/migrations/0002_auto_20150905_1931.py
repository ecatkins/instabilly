# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NearestNeigh',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('distance', models.FloatField()),
                ('neighbor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to='spotify.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='neighs',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='spotify.NearestNeigh', related_name='neighs'),
        ),
    ]
