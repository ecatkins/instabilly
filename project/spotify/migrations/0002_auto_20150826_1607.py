# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistrating',
            name='score',
            field=models.DecimalField(default=0.5, max_digits=6, decimal_places=4),
        ),
    ]
