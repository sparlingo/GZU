# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_playergame'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='season',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='league.Season'),
        ),
    ]
