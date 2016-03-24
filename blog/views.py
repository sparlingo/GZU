from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.utils.safestring import mark_safe

from .models import Post, Comment, Feedback, Question, Choice, Vote
from .models import UserProfile
from .forms import PostForm, CommentForm, FeedbackForm, UserRegistrationForm
from .forms import UserProfileForm
from .forms import VoteForm


from league.models import Player, Season

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
			new_user = authenticate(username=request.POST['username'],
				password=request.POST['password1'])
			# Save to the user_profile table
			profile = form_profile.save(commit=False)
			profile.user = user
			profile.save()
			if user.is_active:
				login(request, new_user)
				messages.add_message(request, messages.SUCCESS, 
					"You are now logged into your new account")
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.INFO, "This account is not active"),
	else:
		form = UserRegistrationForm()
		#form_profile = UserProfileForm()
	return render(request, 'blog/register.html', 
		{
			'form': form,
			#'form_profile': form_profile,
			'title': 'Register',
			'year': datetime.now().year,
		}
	)
		

# Blog Views
@login_required
@csrf_protect
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

@login_required
@csrf_protect
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_view', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', 
			{
				'form': form,
				'title': 'Edit this post',
                'post': post,
			}
		)

def post_index(request): #have to update this and make it more work for all future league
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    latest_season = Season.objects.last()
    max_players =  latest_season.max_male + latest_season.max_female
    existing_player = False
    already = (Player.objects.filter(season_id=latest_season.id)).count()
    if (latest_season.registration_start < timezone.now() < latest_season.registration_end):
        if request.user.is_authenticated():
            if Player.objects.filter(user_id=request.user.id).exists():
                existing_player = True
                messages.info(request, 'YOU ARE REGISTERED! See you on the field')
        
        if (already <= max_players) and (existing_player is False):
            messages.info(request, mark_safe(
                '<a href="league/player/new">Click here to register for 2016 "Baby" League</a>'))
                #'<a href="league/player/new">Click here to register for %s %s League</a>')
                #% (latest_season.year, latest_season.season_of_the_year))
        elif already >= max_players:
            if (latest_season.nickname is not None):
                messages.info(request, "%s %s League is now full" 
                % (latest_season.year, latest_season.nickname))
            else:
                messages.info(request, "%s %s League is now full" 
                % (latest_season.year, latest_season.season_of_the_year))   
          
    
    return render(request, 'blog/post_index.html', 
        {
            'posts': posts,
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def post_view(request, pk):
	post = get_object_or_404(Post, pk=pk)
	comments = Comment.objects.filter(post=post)
	count = len(comments)
	form = CommentForm()
	return render(request, 'blog/post_view.html', 
		{
			'post': post,
			'title': 'News Post',
			'year': datetime.now().year,
			'comments': comments,
			'count': count,
			'form': form,
		}
	)
         
   
# type variable describes what type of object you are commenting on
@login_required
@csrf_protect
def comment_add(request, pk, type):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_id = request.user.id
            if (type == "album"):
                comment.album_id = pk
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Your comment has been saved")
                return HttpResponseRedirect(reverse(album_view, args=[pk]))
            elif (type == "post"):
                comment.post_id = pk
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Thank you for adding to the conversation")
                return HttpResponseRedirect(reverse(post_view, args=[pk]))
            elif (type == "photo"):
                comment.photo_id = pk
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Your comment has been saved")
                return HttpResponseRedirect(reverse(photo_view, args=[pk]))
            elif (type == "question"):
                comment.question_id = pk
                comment.save()
                messages.add_message(request, messages.SUCCESS, "Your comment has been saved")
                return HttpResponseRedirect(reverse(poll_view, args=[pk]))
    else:
        form = CommentForm()

def contact(request): # This also handles the feedback form
	if request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			feedback = form.save()
			feedback.save()
			messages.add_message(request, messages.SUCCESS, 
				"Thank you for telling us what you think, we appreciate it :)")
			return redirect('blog.views.contact')
	else:
		form = FeedbackForm()
		return render(request, 'blog/contact.html', 
			{
				'title':'Contact',
				'message':'Your contact page.',
				'year':datetime.now().year,
				'form': form
			}
		)

def about(request):
	assert isinstance(request, HttpRequest)
	message = 'If you want to play Ultimate Frisbee around Guangzhou, China, we can help.'
	return render(request, 'blog/about.html',
	        context_instance = RequestContext(request,
	        {
	        	'title':'Ultimate around Guangzhou',
	        	'message': message,
	        	'year': datetime.now().year,
	        }
			)
	)

# Views for the photo functions
@login_required
@csrf_protect
def album_new(request):
    if request.method == "POST":
        form = AlbumUploadForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner_id = request.user.id
            album.save()
            return HttpResponseRedirect(reverse(album_view, args=[album.id]))
    else:
        form = AlbumUploadForm()
        return render(request, 'photos/album_new.html', 
            {
                'form': form,
                'title': 'Photos',
                'year': datetime.now().year,
            }
        )

def album_view(request, id):
    album = Album.objects.get(id=int(id))
    comments = Comment.objects.filter(album=album)
    count = len(comments)
    return render(request, 'photos/album_view.html',
        {
            'album': album,
            'title': 'Photo Album',
            'comments': comments,
            'count': count,
            'year': datetime.now().year,
        }
        #context_instance = RequestContext(request)
    )

@login_required
@csrf_protect
def photo_upload(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('file'):
                new_photo = Photos(filename = request.FILES['filename'])
                new_photo.save()
                return HttpResponse('Image(s) uploaded successfully')
    else:
        form = PhotoUploadForm
        
    data = {
        'form': form,
        'album': album,
        }
    return render_to_response('photos/photos_upload.html', 
        data, 
        context_instance=RequestContext(request))

def photo_index(request):
    all_albums = Album.objects.order_by('-created')
    return render(request, 'photos/photos_index.html',
        {
            'all_albums': all_albums,
            'year': datetime.now().year,
            'title': 'Photos',
        }
    )
# Views for the polling function
def poll_index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	return render(request, 'polls/poll_index.html',
	   {
	       	'latest_question_list': latest_question_list,
	       	'year': datetime.now().year,
	       	'title': 'Polls',
	   }
	)

@login_required
@csrf_protect
def poll_view(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        comments = Comment.objects.filter(question=question)
        count = len(comments)
        if request.method == 'POST':
            form = VoteForm(request.POST)
            if form.is_valid():
                vote = form.save(commit=False)
                vote.user = request.user
                vote.save()
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS, "Your vote has been saved")
                return HttpResponseRedirect(reverse(poll_results, args=[question_id]))
        else:
            form = VoteForm()
            #messages.add_message(request, messages.ERROR, "Please try again")
            return render(request, 'polls/poll_view.html',
                {
                    'form': form,
                    'question': question,
                    'choices': choices,
                    'year': datetime.now().year,
                    'title': 'Polls',
                    'comments': comments,
                    'count': count
                    #'errors': errors
                }
            )

def poll_results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	choices = Choice.objects.filter(question_id=question_id)
	for choice in choices:
		votes = Vote.objects.filter(choice__id=choice.id)
		choice.vote_num = len(votes)
	return render(request, 'polls/poll_results.html',
			{
				'question': question,
	        	'choices': choices,
	        	'votes': votes,
				'year': datetime.now().year,
	        	'title': 'Poll Results',
	        }
    )