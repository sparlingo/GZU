from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Season, Team, Player

class PlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ('skill',)