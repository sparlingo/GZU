# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_auto_20150906_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='season',
            old_name='regend',
            new_name='registration_end',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='regstart',
            new_name='registration_start',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='seasonoftheyear',
            new_name='season_of_the_year',
        ),
        migrations.AlterField(
            model_name='season',
            name='slug',
            field=models.SlugField(blank=True, max_length=25),
        ),
    ]
