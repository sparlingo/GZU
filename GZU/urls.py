"""GZU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views
from datetime import datetime
import blog.views, league.views



urlpatterns = [
	# Admin URLs
    url(r'^admin/', admin.site.urls),
	
	# Blog URLs
	url(r'^$', blog.views.post_index, name='home'),
	url(r'^post/(?P<pk>[0-9]+)/$', blog.views.post_view, name='post_view'),
	url(r'^post/edit/(?P<pk>[0-9]+)/$', blog.views.post_edit, name='post_edit'),
	url(r'^post/new/$', blog.views.post_new, name='post_new'),
	
	# League URLs
    url(r'^league/$', league.views.league_index, name='league_index'),
	url(r'^league/schedule/(?P<pk>[0-9]+)/$', league.views.schedule, name='schedule'),
	url(r'^league/schedule/(?P<pk>[0-9]+)/team/(?P<team_id>[0-9]+)/$', league.views.schedule, name='team_schedule'),
	url(r'^league/player/new/$', league.views.player_new, name='player_new'),
	url(r'^league/scores/(?P<pk>[0-9]+)/$', league.views.scores, name='scores'),
	url(r'^league/scores/(?P<pk>[0-9]+)/team/(?P<team_id>[0-9]+)/$', league.views.scores, name='team_scores'),
    url(r'^league/score/edit/(?P<game_id>[0-9]+)/(?P<team_id>[0-9]+)/$', league.views.score_edit, name='score_edit'),
    url(r'^league/score/(?P<game_id>[0-9]+)/$', league.views.score_view, name='score_view'),
    url(r'^league/stats/(?P<game_id>[0-9]+)/(?P<team_id>[0-9]+)/$', league.views.stats_report, name='stats_report'),
    url(r'^league/stats/edit/(?P<game_id>[0-9]+)/(?P<team_id>[0-9]+)/$', league.views.stats_team_edit, name='stats_team_edit'),
	
	# Comments
	url(r'^comment_add/(?P<pk>[0-9]+)/(?P<type>\w+)/$', blog.views.comment_add, name='comment_add'),
	
	# Picture URLs
    #url(r'^photos$', blog.views.photo_index, name='photos'),
    #url(r'^photos/album/(?P<id>\d+)/$', blog.views.album_view, name='album_view'),
    #url(r'^photos/album/new$', blog.views.album_new, name='album_new'),
    #url(r'^photos/photo_upload/(?P<id>\d+)/$', blog.views.photo_upload, name='photo_upload'),
    
    # Photos URLs
    #url(r'^$', lambda x: HttpResponseRedirect('pictures/upload/new/')),
    #url(r'^photos/', include('photos.urls')),
	
	# Poll URLs
	url(r'^polls$', blog.views.poll_index, name='polls'),
	url(r'^poll/(?P<question_id>[0-9]+)/$', blog.views.poll_view, name='poll_view'),
	url(r'^poll/(?P<question_id>[0-9]+)/results/$', blog.views.poll_results, name='poll_results'),
	#url(r'^poll/(?P<question_id>[0-9]+)/vote/$', 'polls.views.poll_vote', name='poll_vote'),
	
	# Static pages URLs
    url(r'^contact$', blog.views.contact, name='contact'),
    url(r'^about$', blog.views.about, name='about'),
    
	# User URLs
	url(r'^register$', blog.views.register, name='register'),
	url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
]
