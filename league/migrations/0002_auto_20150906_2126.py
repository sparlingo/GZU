# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='jerseyorder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='season',
            name='leagueblurb',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='season',
            name='regprice',
            field=models.PositiveSmallIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='season',
            name='max_female',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='max_male',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
    ]
