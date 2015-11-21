from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
		
class Comment(models.Model):
	author = models.ForeignKey('auth.User')
	text = models.TextField(max_length=500)
	created_date = models.DateTimeField(default=timezone.now)
	post = models.ForeignKey(Post)
	
	def __str__(self):
		return self.text[:80]
		
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
	User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u) [0])
		
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
	