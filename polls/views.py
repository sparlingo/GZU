from django.shortcuts import HttpResponse, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User



from .models import Question, Choice

def poll_index(request):
	#if user.is_authenticated:
		latest_question_list = Question.objects.order_by('-pub_date')[:5]
		context = {'latest_question_list': latest_question_list}
		return render(request, 'polls/poll_index.html', context)
"""else:
		messages.add_message(request, messages.ERROR, "You must be logged in to vote. Please use the links at the top to login or register")
		return HttpResponseRedirect('/')"""

def poll_detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/poll_detail.html', {'question': question})
	
def poll_results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	
def poll_vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/poll_detail.html', {
			'question': p,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#return HttpResponseRedirect(reverse('polls/poll_results.html', args=(p.id)))
		question = get_object_or_404(Question, pk=question_id)
		return render(request, 'polls/poll_results.html', {'question': question})