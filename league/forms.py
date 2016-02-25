from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Season, Team, Player, Game, PlayerGame

class PlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ('first_year_frisbee',)
        
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('homescore', 'awayscore', 'homespirit', 'awayspirit',)
        
class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = PlayerGame
        exclude = ('multiplier', 'game_id', 'player_id', 'team_id',)

class TeamStatsForm(forms.Form):
    passes = forms.IntegerField()
    assists = forms.IntegerField()
    points = forms.IntegerField()
    defences = forms.IntegerField()
    drops = forms.IntegerField()
    throwaways = forms.IntegerField()
    multiplier = forms.FloatField()
    player_id = forms.IntegerField()
