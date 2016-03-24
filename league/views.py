from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django_tables2 import RequestConfig
from .tables import GameTable, ScoreTable, PlayerStatsTable


from .models import Season, Team, Player, Field, Game, PlayerStat
from .forms import PlayerForm, ScoreForm, PlayerStatsForm, TeamStatsForm

def league_index(request):
    
    return render(request, 'league/index.html',
        {
            'title': 'League',
        }
    )

def schedule(request, pk, team_id=0):
	season = get_object_or_404(Season, pk=pk)
	
	if (team_id != 0):
		today = datetime.today()
		endofweek = datetime.today() + timedelta(days=6)
		games_thisweek = GameTable(Game.objects.filter(
			Q(game_end__range=[today, endofweek]) & Q(season_id=pk) 
			& (Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
			)
		)
		RequestConfig(request).configure(games_thisweek)
	
		nextweek_start = datetime.today() + timedelta(days=7)
		nextweek_end = nextweek_start + timedelta(days=7)
		games_nextweek = GameTable(Game.objects.filter(
			Q(game_end__range=[nextweek_start, nextweek_end]) & Q(season_id=pk)
			& (Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
			)
		)
		RequestConfig(request).configure(games_nextweek)
	else:
		today = datetime.today()
		endofweek = datetime.today() + timedelta(days=6)
		games_thisweek = GameTable(Game.objects.filter(
			Q(game_end__range=[today, endofweek]) & Q(season_id=pk) 
			)
		)
		RequestConfig(request).configure(games_thisweek)
	
		nextweek_start = datetime.today() + timedelta(days=7)
		nextweek_end = nextweek_start + timedelta(days=7)
		games_nextweek = GameTable(Game.objects.filter(
			Q(game_end__range=[nextweek_start, nextweek_end]) & Q(season_id=pk)
			)
		)
		RequestConfig(request).configure(games_nextweek)
	
	return render(request, 'league/schedule.html',
		{
			'title': 'League Schedule',
			'games_thisweek': games_thisweek,
			'games_nextweek': games_nextweek,
			'season': season,
		}
	)
	
def scores(request, pk, team_id=0):
	season = get_object_or_404(Season, pk=pk)
	
	if (team_id != 0):
		scores = ScoreTable(Game.objects.filter(
			(Q(season_id=pk)
			& (Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
			)).exclude(game_end__gte=datetime.now())
		)
		RequestConfig(request).configure(scores)
	else:
		scores = ScoreTable(Game.objects.filter(
			season_id=pk).exclude(game_end__gte=datetime.now()
			)
		)
		RequestConfig(request).configure(scores)
		
		
	return render(request, 'league/scores.html',
		{
			'title': 'League Scores',
			'scores': scores,
			'season': season,
		}
	)

@login_required #This could be done more gracefully, KS: Feb13, 2016
@csrf_protect #Why doesn't it load the existing value?
def score_edit(request, game_id, team_id):
    thisgame = get_object_or_404(Game, pk=game_id)
    hometeam = Team.objects.get(pk=team_id)
    awayteam = Team.objects.get(pk=team_id)
    
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=thisgame)
        if form.is_valid():
            score = form.save()
            return HttpResponseRedirect(reverse(score_view, args=[thisgame.id]))
    else:
        form = ScoreForm(instance=thisgame)
        if (hometeam != None) and (hometeam.captain_id == request.user.id):
            return render(request, 'league/score_edit.html',
                {
                    'title': 'Report game results',
                    'thisgame': thisgame,
                    'form': form,
                    'hometeam': hometeam
                }
            )
        elif (awayteam != None) and (awayteam.captain_id == request.user.id):
            return render(request, 'league/score_edit.html',
                {
                    'title': 'Report game results',
                    'thisgame': thisgame,
                    'form': form,
                    'awayteam': awayteam
                }
            )    
        
def score_view(request, game_id):
    thisgame = get_object_or_404(Game, pk=game_id)
    
    return render(request, 'league/score_view.html',
        {
            'title': 'Game Result',
            'thisgame': thisgame,
        }
    )
    

@login_required
def player_new(request, season_id=None): #have to update this for all leagues
    thisseason = Season.objects.last()
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user_id = request.user.id
            player.team_id = 0
            player.season_id = thisseason.id
            player.save()
            return HttpResponseRedirect('/')
    else:
        form = PlayerForm()
        """if (thisseason.nickname is not None):
            titlestring = 'Register for %s %s League' % (thisseason.year, thisseason.nickname)
        else:
            titlestring = 'Register for %s %s League' % (thisseason.year. thisseason.season_of_the_year)"""
        return render(request, 'league/player_new.html', 
            {
                'form': form,
                'title': 'Register for 2016 "Baby" League',
            }
        )

@login_required
def stats_report(request, game_id, team_id): #update so you can view stats for whole season
    for player in Player.objects.filter(team_id=team_id):
        try:
            obj = PlayerStat.objects.get(player_id=player.id, game_id=game_id, team_id=team_id)
        except PlayerStat.DoesNotExist:
            obj = PlayerStat(player_id=player.id, game_id=game_id, team_id=team_id)
            obj.save()
    
    teamgamestats = PlayerStatsTable(PlayerGame.objects.filter(
            Q(game_id=game_id) & Q(team_id=team_id)))
    thisteam = Team.objects.get(pk=team_id)
    thisgame = Game.objects.get(pk=game_id)
    RequestConfig(request).configure(teamgamestats)
    
    return render(request, 'league/stats_view.html',
        {
            'title': 'Team Stats',
            'teamgamestats': teamgamestats,
            'thisteam': thisteam,
            'thisgame': thisgame,
            'year': datetime.now().year,
        }
    )  

        
@login_required
@csrf_protect
def stats_team_edit(request, game_id, team_id):
    playerstats = PlayerGame.objects.filter(
        Q(game_id=game_id) & Q(team_id=team_id))
    TeamStatsFormSet = formset_factory(TeamStatsForm, extra=15)
    if request.method == "POST":
        formset = TeamStatsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            playerstats = formset.save(commit=False)
            playerstats.save()
            #pass
            return HttpResponseRedirect(reverse(stats_report, args=[game_id, team_id]))
    else:
        formset = TeamStatsFormSet()
        return render(request, 'league/stats_team_edit.html',
            {
                'formset': formset,
                'title': 'Team Stats',
                'playerstats': playerstats,
            }
        )
          


@login_required
@csrf_protect
def stats_player_edit(request, team_id, player_id):
    playerstats = PlayerGame.objects.filter()# obviously needs to change
    if request.method == "POST":
        form = PlayerStatsForm(request.POST)
        if form.is_valid():
            playerstats = form.save(commit=False)
            playerstats.save()
            return HttpResponseRedirect(reverse(stats_view, args=[game_id]))
    else:
        form = PlayerStatsForm() # need to lookup and pass stats_edit
        return render(request, 'league/stats_edit.html',
            {
                'form': form,
                'title': 'Player Stats',
                'playerstats': playerstats,
            }
        )