from django.db import models
from django import forms
from django.utils import timezone


# Models for blog
class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=500)
	text = models.TextField()
	created_date = models.DateTimeField(
		default=timezone.now)
	published_date = models.DateTimeField(
		blank=True, null=True)
		
	def publish(self):
		self.published_date = timezone.now()
		self.save()
		
	def __str__(self):
		return self.title

""""		
class Artist(models.Model):
    name = models.CharField("artist", max_length=50)
    year_formed = models.PositiveIntegerField()

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist;
        fields = ['name', 'year_formed'];

class Album(models.Model):
    name = models.CharField("album", max_length=50)
    artist = models.ForeignKey(Artist)
"""
