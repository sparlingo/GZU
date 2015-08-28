from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.utils import timezone
from .models import *
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
			email = form.cleaned_data['email'],
			)
			user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, "You are now logged into your new account")
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.INFO, "This account is not active"),
	else:
		form = RegistrationForm()
	return render(request, 'blog/register.html', 
		{
			'form': form,
			'title': 'Register',
			'year': datetime.now().year,
		})
		
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
			return redirect('blog.views.post_detail', pk=post.pk)
		else:
			form = PostForm()
	return render(request, 'blog/post_new.html', {'form': form})

"""	I'll update this later - KS, Aug 24, 2015
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})
"""
def post_index(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(
		request, 
		'blog/post_index.html', 
		{
			'posts': posts,
			'title': 'Home Page',
			'year': datetime.now().year,
		})
		
def post_view(request, pk):
	post = get_object_or_404(Post, pk=pk)
	comments = Comment.objects.filter(post=post)
	return render(
		request, 
		'blog/post_view.html', 
		{
			'post': post,
			'title': 'News Post',
			'year': datetime.now().year,
			'comments': comments,
		})


""" Re-enable this if you don't want the blog index on the website root
def home(request):
 
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'blog/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )
"""
def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'blog/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'blog/about.html',
        context_instance = RequestContext(request,
        {
            'title':'Ultimate around Guangzhou',
            'message':'If you want to play Ultimate Frisbee around Guangzhou, China, we can help.',
            'year':datetime.now().year,
        })
    )
