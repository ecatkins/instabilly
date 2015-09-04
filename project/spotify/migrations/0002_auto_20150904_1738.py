# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nearestneighbor',
            name='id',
        ),
        migrations.AlterField(
            model_name='nearestneighbor',
            name='user',
            field=models.OneToOneField(serialize=False, to='spotify.UserProfile', primary_key=True),
        ),
    ]
