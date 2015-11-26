from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


from .models import Season, Team, Player, Field, Game
from .forms import PlayerForm

#Obviously needs to be updated
@login_required
def player_new(request):
	if request.method == "POST":
		form = PlayerForm(request.POST)
		if form.is_valid():
			player = form.save(commit=False)
			player.user_id = request.user.id
			player.team_id = 1
			player.save()
			return HttpResponseRedirect('/')
	else:
		form = PlayerForm()
		return render(request, 'league/player_new.html', 
			{
				'form': form,
				'title': 'Register for Fall League 2015',
			}
		)