"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Blog Views

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('app.views.post_list')
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
	return render(request, 'app/post_list.html', {'posts': posts})
	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'app/post_detail.html', {'post': post})


def artistcreate(request):
    if request.method == "GET":
        form = ArtistForm();
        return render(request, 'app/create.html', { 'form':form });
    elif request.method == "POST":
        form = ArtistForm(request.POST);
        form.save();
        return HttpResponseRedirect('/artists');

def artists(request):
    artists = Artist.objects.all();
    return render_to_response('app/artists.html', {'artists': artists});

def artistdetails(request, id):
    artist = Artist.objects.get(pk = id);
    return render_to_response('app/artistdetails.html', { 'artist': artist });
    
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
