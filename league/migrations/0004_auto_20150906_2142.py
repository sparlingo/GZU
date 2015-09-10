# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_auto_20150906_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='season',
            old_name='regprice',
            new_name='registration_price',
        ),
    ]
