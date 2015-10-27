from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .models import *
from .forms import *

# User Views

@csrf_protect
def register(request): #Clean this up later, KS 2015/09/08
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		form_profile = UserProfileForm(request.POST)
		if form.is_valid() and form_profile.is_valid():
			# Save to the auth_user table
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email'],
			)
			# login the new user, might want to add email authentication in the future
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			# Save to the user_profile table
			profile = form_profile.save(commit=False)
			profile.user = user
			profile.save()
			if user.is_active:
				login(request, new_user)
				messages.add_message(request, messages.SUCCESS, "You are now logged into your new account")
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.INFO, "This account is not active"),
	else:
		form = UserRegistrationForm()
		form_profile = UserProfileForm()
	return render(request, 'blog/register.html', 
		{
			'form': form,
			'form_profile': form_profile,
			'title': 'Register',
			'year': datetime.now().year,
		})
		

# Blog Views
@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return HttpResponseRedirect('/')
	else:
		form = PostForm()
		return render(request, 'blog/post_new.html', 
			{
			'form': form,
			'title': 'Create a news post',
			}
		)

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
		return render(request, 'blog/post_edit.html', 
			{
			'form': form,
			'title': 'Edit this post',
			}
		)

def post_index(request):
	# Change the filter to only grab the first 100 characters or something to keep the homepage clean
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	# Add something later to simply show how many comments there are for each news post
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
	count = len(comments)
	form = CommentForm
	return render(
		request, 
		'blog/post_view.html', 
		{
			'post': post,
			'title': 'News Post',
			'year': datetime.now().year,
			'comments': comments,
			'count': count,
			'form': form,
		}
	)

# Have to modify this so that it works for multiple types
@csrf_protect
def comment_add(request, pk):
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post_id = pk
			comment.author_id = request.user.id
			comment.save()
			messages.add_message(request, messages.SUCCESS, "Thank you for adding to the conversation")
			return HttpResponseRedirect(reverse(post_view, args=[pk]))
	else:
		form = CommentForm()

def contact(request): # This also handles the feedback form
	if request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			feedback = form.save()
			messages.add_message(request, messages.SUCCESS, "Thank you for telling us what you think, we appreciate it :)")
			return redirect('blog.views.contact')
	else:
		form = FeedbackForm()
		return render(
			request, 'blog/contact.html', {
				'title':'Contact',
				'message':'Your contact page.',
				'year':datetime.now().year,
				'form': form
			}
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

def photos(request):
	return render(
		request,
		'blog/photos.html',
		{
			'title': 'Photos',
			'year': datetime.now().year,
		}
	)

# Views for the polling function
def poll_index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	return render(request, 
	        'polls/poll_index.html',
	        {
	                'latest_question_list': latest_question_list,
	                'year': datetime.now().year,
	                'title': 'Polls',
	        }
	)

@login_required
@csrf_protect
def poll_detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	choices = Choice.objects.filter(question_id=question_id)	
	if request.method == 'POST':
		form = VoteForm(request.POST)
		if form.is_valid():
			vote = form.save(commit=False)
			vote.user = request.user
			vote.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse(poll_results, args=[question_id]))
		else:
			form = VoteForm()
			messages.add_message(request, messages.ERROR, "Please try again")
			return render(request,
			        'polls/poll_detail.html',
			        {
			                'form': form,
			                'question': question,
			                'choices': choices,
			                'year': datetime.now().year,
			                'title': 'Polls',
			                #'errors': errors
			        }
			)
	else:
		form = VoteForm()
		return render(request, 
		        'polls/poll_detail.html', 
		        {
		                'form': form,
		                'question': question,
		                'choices': choices,
		                'year': datetime.now().year,
		                'title': 'Polls',
		        }
		)

def poll_results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	choices = Choice.objects.filter(question_id=question_id)
	for choice in choices:
		votes = Vote.objects.filter(choice__id=choice.id)
		choice.vote_num = len(votes)
	#votes = Vote.objects.all()
	return render(request,
	        'polls/poll_results.html',
		{
			'question': question,
	                'choices': choices,
	                'votes': votes,
			'year': datetime.now().year,
	                'title': 'Poll Results',
	        }
	)