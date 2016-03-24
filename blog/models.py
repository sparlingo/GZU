from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Models for blog
class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=80, blank=False, null=False)
	text = models.TextField(max_length=2000,)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
		
	def publish(self):
		self.published_date = timezone.now()
		self.save()
		
	def __str__(self):
		return self.title
				
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=20)
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    name = models.CharField(max_length=30, blank=True, null=True)
    name_international = models.CharField(max_length=15, blank=True, null=True)
    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u) [0])

    def __str__(self):
        return self.name
	
class Feedback(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
	
    def __str__(self):
        return self.text[:25]
	
# Models for polls
class Question(models.Model):
    question_text = models.CharField(max_length=100)
    question_reference = models.CharField(max_length=50)
    question_set = models.PositiveSmallIntegerField('question set', blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    expire_date = models.DateTimeField('expiry date')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)

	def __str__(self):
		return self.choice_text

class Vote(models.Model):
	user = models.ForeignKey(User)
	choice = models.ManyToManyField(Choice)	
    
class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, blank=True, null=True)
    #photo = models.ForeignKey(Photo, blank=True, null=True)
    #album = models.ForeignKey(Album, blank=True, null=True)
    question = models.ForeignKey(Question, blank=True, null=True)
    
    def __str__(self):
        return self.text[:80]