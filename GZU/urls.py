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
from datetime import datetime


urlpatterns = [
	# Admin URLs
    url(r'^admin/', include(admin.site.urls)),
	
	
	# Blog URLs
	url(r'^$', 'blog.views.post_index', name='home'),
	url(r'^post/new/$', 'blog.views.post_new', name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/$', 'blog.views.post_view', name='post_view'),
	
	# Poll URLs
	url(r'^polls$', 'polls.views.poll_index', name='polls'),
	url(r'^poll/(?P<question_id>[0-9]+)/$', 'polls.views.poll_detail', name='poll_detail'),
	url(r'^poll/(?P<question_id>[0-9]+)/results/$', 'polls.views.poll_results', name='poll_results'),
	url(r'^poll/(?P<question_id>[0-9]+)/vote/$', 'polls.views.poll_vote', name='poll_vote'),
	
	# Static pages URLs
    url(r'^contact$', 'blog.views.contact', name='contact'),
    url(r'^about', 'blog.views.about', name='about'),
    
	# User URLs
	url(r'^register', 'blog.views.register', name='register'),
	url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
]