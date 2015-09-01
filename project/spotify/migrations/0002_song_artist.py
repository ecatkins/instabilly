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
            name='artist',
            field=models.CharField(default='None', max_length=200),
            preserve_default=False,
        ),
    ]
