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
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('field_name', models.CharField(max_length=25)),
                ('slug', models.SlugField(blank=True, max_length=25)),
                ('directions', models.CharField(null=True, blank=True, max_length=250)),
                ('field_lat', models.FloatField(null=True, blank=True)),
                ('field_long', models.FloatField(null=True, blank=True)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('url', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('game_start', models.DateTimeField()),
                ('game_end', models.DateTimeField()),
                ('homescore', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('awayscore', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('homespirit', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('awayspirit', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('slug', models.SlugField(blank=True, max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('jersey', models.CharField(null=True, blank=True, max_length=2)),
                ('skill', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('season_of_the_year', models.CharField(choices=[('SP', 'Spring'), ('SU', 'Summer'), ('F', 'Fall'), ('W', 'Winter')], max_length=2)),
                ('registration_start', models.DateTimeField(auto_now=True)),
                ('registration_end', models.DateTimeField()),
                ('registration_price', models.PositiveSmallIntegerField(default='0')),
                ('max_female', models.PositiveSmallIntegerField(blank=True)),
                ('max_male', models.PositiveSmallIntegerField(blank=True)),
                ('slug', models.SlugField(max_length=25)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('jerseyorder', models.NullBooleanField()),
                ('commish', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('team_name', models.CharField(max_length=50)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=25)),
                ('captain', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(to='league.Season')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='league.Team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='awayteam',
            field=models.ForeignKey(to='league.Team', related_name='game_awayteam'),
        ),
        migrations.AddField(
            model_name='game',
            name='field',
            field=models.ForeignKey(to='league.Field'),
        ),
        migrations.AddField(
            model_name='game',
            name='hometeam',
            field=models.ForeignKey(to='league.Team', related_name='game_hometeam'),
        ),
    ]
