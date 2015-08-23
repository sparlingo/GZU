"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.utils import timezone
from .models import Post
from .forms import *

# User Views

@csrf_protect
def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username = form.cleaned_data['username'],
			password = form.cleaned_data['password1'],
			email = form.cleaned_data['email']
			)
			#-return HttpResponseRedirect('/success/')
	else:
		form = RegistrationForm()
	return render(request, 'app/register.html', 
		{
			'form': form,
			'title': 'Register',
			'year': datetime.now().year,
		})
	
def register_success(request):
	return render_to_response('success.html')
	
@login_required
def home(request):
	return render_to_response('home.html', {'user': request.user})

# Blog Views

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('app.views.post_detail', pk=post.pk)
		else:
			form = PostForm()
	return render(request, 'app/post_new.html', {'form': form})
		
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('app.views.post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'app/post_edit.html', {'form': form})
	
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(
		request, 
		'app/post_list.html', 
		{
			'posts': posts,
			'title': 'Home Page',
			'year': datetime.now().year,
		})
		
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(
		request, 
		'app/post_detail.html', 
		{
			'post': post,
			'title': 'News Post',
			'year': datetime.now().year,
		})


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
