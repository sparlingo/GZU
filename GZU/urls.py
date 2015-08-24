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
from blog.forms import BootstrapAuthenticationForm
from datetime import datetime

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	
	url(r'^register', 'blog.views.register', name='register'),
	
	url(r'^$', 'blog.views.post_index', name='post_index'),
	url(r'^post/new/$', 'blog.views.post_new', name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/$', 'blog.views.post_view', name='post_view'),
	
	url(r'^polls$', 'polls.views.index', name='index'),
	
    url(r'^contact$', 'blog.views.contact', name='contact'),
    url(r'^about', 'blog.views.about', name='about'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'blog/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
]