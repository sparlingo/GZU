from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .models import Post, Comment, Feedback, UserProfile


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text')
		
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
		
class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ('text',)
		
class UserRegistrationForm(forms.ModelForm):
	username = forms.CharField(max_length=20, required=True)
	email = forms.EmailField(max_length=30, required=True)
	password1 = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput())
	password2 = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
	def clean_username(self):
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError(_("The username already exists. Please try another one."))
 
	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields did not match."))
		return self.cleaned_data

	
class UserProfileForm(forms.ModelForm):
	gender_choices = (		
		('M', 'Male'),
		('F', 'Female'),
	)
	gender = forms.ChoiceField(
		label='Please indicate a gender', choices=gender_choices, widget=forms.RadioSelect()
	)
	class Meta:
		model = UserProfile
		fields = ('gender', )