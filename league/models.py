from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Season(models.Model):
	commish = models.ForeignKey('auth.User')
	
	SPRING = 'Spring'
	SUMMER = 'Summer'
	FALL = 'Fall'
	WINTER = 'Winter'
	SOTY_CHOICES = (
		(SPRING, 'Spring'),
		(SUMMER, 'Summer'),
		(FALL, 'Fall'),
		(WINTER, 'Winter')
	)
	season_of_the_year = models.CharField(max_length=6, choices = SOTY_CHOICES)
	YEAR_CHOICES = []
	for r in range(1990, (datetime.now().year+2)):
		value = [r, r]
		YEAR_CHOICES.append(value)
	year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
	nickname = models.CharField(max_length=20, blank=True, null=True)
	registration_start = models.DateTimeField()
	registration_end = models.DateTimeField()
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
    stats_url = models.CharField(max_length=200, blank=True, null=True)
    
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
	hometeam = models.ForeignKey(Team, related_name='game_hometeam', verbose_name="Home Team")
	awayteam = models.ForeignKey(Team, related_name='game_awayteam', verbose_name="Away Team")
	season = models.ForeignKey(Season)
	game_start = models.DateTimeField(
		auto_now=False, blank=False, null=False, 
		verbose_name="Start Time",
	)
	game_end = models.DateTimeField(
		auto_now=False, blank=False, null=False, 
		verbose_name="End Time"
	)
	field = models.ForeignKey(Field, verbose_name="Field")
	homescore = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Home Team Score')
	awayscore = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Away Team Score')
	homespirit = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Home Team Spirit')
	awayspirit = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Away Team Spirit')
	slug = models.SlugField(max_length=25, blank=True)
	
	def __str__(self):
		return u"%s vs %s @ %s" % (self.hometeam, self.awayteam, self.field)

class Player(models.Model):
    year_dropdown = []
    for y in range(1980, (datetime.now().year + 1)):
        year_dropdown.append((y, y))
        
    user = models.ForeignKey('auth.User')
    team = models.ForeignKey(Team)
    season = models.ForeignKey(Season, default=0)
    jersey = models.CharField(max_length=2, blank=True, null=True)
    skill = models.PositiveSmallIntegerField(blank=True, null=True)
    first_year_frisbee = models.IntegerField(('year'), choices=year_dropdown, default=datetime.now().year)
    notes = models.CharField(max_length=400, blank=True, null=True)
	
    def __str__(self):
        return self.user.username
        
class PlayerStat(models.Model):
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game)
    passes = models.PositiveSmallIntegerField(blank=True, null=True)
    catches = models.PositiveSmallIntegerField(blank=True, null=True)
    assists = models.PositiveSmallIntegerField(blank=True, null=True)
    points = models.PositiveSmallIntegerField(blank=True, null=True)
    defences = models.PositiveSmallIntegerField(blank=True, null=True)
    drops = models.PositiveSmallIntegerField(blank=True, null=True)
    throwaways = models.PositiveSmallIntegerField(blank=True, null=True)
    multiplier = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return u"%s - %s - %s" % (self.player, self.team, self.game)