# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('seasonoftheyear', models.CharField(max_length=2, choices=[('SP', 'Spring'), ('SU', 'Summer'), ('F', 'Fall'), ('W', 'Winter')])),
                ('regstart', models.DateTimeField()),
                ('regend', models.DateTimeField()),
                ('max_female', models.PositiveSmallIntegerField()),
                ('max_male', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField(max_length=25)),
                ('commish', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
