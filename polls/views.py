from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse

from .models import Choice, Question

"""
Without generic view

def index(request):
    last_question_list = Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        "latest_question_list" : last_question_list,
    }
    # return HttpResponse(template.render(context,request))
    return render(request,"polls/index.html",context)
    # output = ", ".join([q.question_text for q in last_question_list])
    # return HttpResponse(output)


def detail(request,question_id):
    # The view raises the Http404 exception if a question with the requested ID doesn’t exist.
    
    # try:
        # question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
        # raise Http404("Question does not exist")
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request,"polls/detail.html",{"question":question})
    # return HttpResponse("You'e looking at question %s."%question_id)


def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,"polls/results.html",{"question":question})
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response%question_id)
"""

# Display a list of the latest questions.
# generic.ListView base class is a generic view for displaying a list of object
# ListView generic view uses a default template called <app name>/<model name>_list.html
class IndexView(generic.ListView):
    # template_name specifies the template file used to render the view.
    template_name = "polls/index.html"
    # context_object_name defines the variable name that will be used in the template to access the list of questions.
    # for ListView, the automatically generated context variable is question_list. To override this we provide the 
    # context_object_name attribute, specifying that we want to use latest_question_list instead. 
    # an alternative approach, you could change your templates to match the new default context variables 
    # – but it’s a lot easier to tell Django to use the variable you want.
    context_object_name = 'latest_question_list'

    # method is overridden to return the last five published questions ordered by their 
    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]

        # returns a queryset containing Questions whose pub_date is less than or equal to rn , earlier than or equal to - timezone.now.
        # here pub_date is the name of of variable and ___lte is lookup used to get records that are less than, or equal to, a specified value
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# generic.DetailView class, which is a generic view for displaying the details of a single object.
# By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html.
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet or getting published in future
        """
        # here pub_date is the name of of variable and ___lte is lookup used to get records that are less than, or equal to, a specified value
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model  = Question
    template_name = 'polls/results.html'
    


# This view handles the logic for processing a user's vote for a specific question.
# question_id is a parameter, which is the ID of the question the user is voting on.
def vote(request,question_id):
    question  = get_object_or_404(Question,pk=question_id)
    # below code will get keyerror if choice not provided
    try:
        # choice_set if used to filter the choices according to a question instance
        # to get only the choices for a particular questions 
        # this can be used as they have one to many relation
        # so we get filter choices and look for choice number using get function
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # if no choice is selected and we get null
    except (KeyError,Choice.DoesNotExist):
        # redisplay the question voting form
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"You didn't select a choice.",
            }
        )
    else:
        # ncrements the vote count if document exists
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # HttpResponseRedirect is  the URL to which the user will be redirected
        # currently we at /polls/5/vote it will reverse to /polls/5/ then go to /polls/5/results
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



