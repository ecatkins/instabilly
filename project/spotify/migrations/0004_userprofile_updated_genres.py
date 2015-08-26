# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0003_auto_20150826_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='updated_genres',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 26, 17, 56, 50, 141634, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
