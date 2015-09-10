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
	registration_start = models.DateTimeField(auto_now=False)
	registration_end = models.DateTimeField(auto_now=False)
	registration_price = models.PositiveSmallIntegerField(default='0')
	max_female = models.PositiveSmallIntegerField(blank=True)
	max_male = models.PositiveSmallIntegerField(blank=True)
	slug = models.SlugField(max_length=25, blank=True)
	leagueblurb = models.CharField(max_length=200, blank=True)
	jerseyorder = models.BooleanField(default=False)

	def __str__(self):
		return self.season_of_the_year