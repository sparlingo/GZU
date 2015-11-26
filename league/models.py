from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Season(models.Model):
	commish = models.ForeignKey('auth.User')
	SPRING = 'SP'
	SUMMER = 'SU'
	FALL = 'F'
	WINTER = 'W'
	SOTY_CHOICES = (
		(SPRING, 'Spring'),
		(SUMMER, 'Summer'),
		(FALL, 'Fall'),
		(WINTER, 'Winter')
	)
	season_of_the_year = models.CharField(max_length=2, choices = SOTY_CHOICES)
	year = datetime.now().year
	registration_start = models.DateTimeField(auto_now=True)
	registration_end = models.DateTimeField(auto_now=False)
	registration_price = models.PositiveSmallIntegerField(default='0')
	max_female = models.PositiveSmallIntegerField(blank=True, null=True)
	max_male = models.PositiveSmallIntegerField(blank=True, null=True)
	slug = models.SlugField(max_length=25)
	blurb = models.CharField(max_length=200, blank=True)
	jerseyorder = models.NullBooleanField(null=True)
	
	def __str__(self):
		return self.slug
		
class Team(models.Model):
	captain = models.ForeignKey('auth.User')
	league = models.ForeignKey(Season)
	team_name = models.CharField(blank=False, max_length=50)
	blurb = models.CharField(max_length=200, blank=True)
	slug = models.SlugField(max_length=25, blank=True)
	
	def __str__(self):
		return self.team_name
		
class Field(models.Model):
	field_name = models.CharField(max_length=25, blank=False, null=False)
	slug = models.SlugField(max_length=25, blank=True)
	directions = models.CharField(max_length=250, blank=True, null=True)
	field_lat = models.FloatField(blank=True, null=True)
	field_long = models.FloatField(blank=True, null=True)
	blurb = models.CharField(max_length=200, blank=True)
	url = models.URLField(blank=True, null=True)
	
	def __str__(self):
		return self.field_name
		
class Game(models.Model):
	hometeam = models.ForeignKey(Team, related_name='game_hometeam')
	awayteam = models.ForeignKey(Team, related_name='game_awayteam')
	game_start = models.DateTimeField(auto_now=False, blank=False, null=False)
	game_end = models.DateTimeField(auto_now=False, blank=False, null=False)
	field = models.ForeignKey(Field)
	homescore = models.PositiveSmallIntegerField(blank=True, null=True)
	awayscore = models.PositiveSmallIntegerField(blank=True, null=True)
	homespirit = models.PositiveSmallIntegerField(blank=True, null=True)
	awayspirit = models.PositiveSmallIntegerField(blank=True, null=True)
	slug = models.SlugField(max_length=25, blank=True)
	
	def __str__(self):
		return self.slug

class Player(models.Model):
	user = models.ForeignKey('auth.User')
	team = models.ForeignKey(Team)
	jersey = models.CharField(max_length=2, blank=True, null=True)
	skill = models.PositiveSmallIntegerField(blank=True, null=True)
	
	def __str__(self):
		return self.user.username