# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artists',
            field=models.ForeignKey(default=1, to='spotify.Artist'),
            preserve_default=False,
        ),
    ]
