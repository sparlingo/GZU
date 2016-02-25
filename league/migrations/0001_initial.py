# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=25)),
                ('slug', models.SlugField(blank=True, max_length=25)),
                ('directions', models.CharField(blank=True, max_length=250, null=True)),
                ('field_lat', models.FloatField(blank=True, null=True)),
                ('field_long', models.FloatField(blank=True, null=True)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_start', models.DateTimeField(verbose_name='Start Time')),
                ('game_end', models.DateTimeField(verbose_name='End Time')),
                ('homescore', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('awayscore', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('homespirit', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('awayspirit', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jersey', models.CharField(blank=True, max_length=2, null=True)),
                ('skill', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_of_the_year', models.CharField(choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'), ('Winter', 'Winter')], max_length=6)),
                ('year', models.PositiveSmallIntegerField(choices=[[1990, 1990], [1991, 1991], [1992, 1992], [1993, 1993], [1994, 1994], [1995, 1995], [1996, 1996], [1997, 1997], [1998, 1998], [1999, 1999], [2000, 2000], [2001, 2001], [2002, 2002], [2003, 2003], [2004, 2004], [2005, 2005], [2006, 2006], [2007, 2007], [2008, 2008], [2009, 2009], [2010, 2010], [2011, 2011], [2012, 2012], [2013, 2013], [2014, 2014], [2015, 2015], [2016, 2016], [2017, 2017]], default=2016)),
                ('registration_start', models.DateTimeField(auto_now=True)),
                ('registration_end', models.DateTimeField()),
                ('registration_price', models.PositiveSmallIntegerField(default='0')),
                ('max_female', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('max_male', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=25)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('jerseyorder', models.NullBooleanField()),
                ('commish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=50)),
                ('blurb', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=25)),
                ('captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Season')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='awayteam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_awayteam', to='league.Team', verbose_name='Away Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Field', verbose_name='Field'),
        ),
        migrations.AddField(
            model_name='game',
            name='hometeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_hometeam', to='league.Team', verbose_name='Home Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Season'),
        ),
    ]
