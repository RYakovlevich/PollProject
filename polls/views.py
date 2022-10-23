from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Question, Choice, ResultTest, Test
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from polls import models


class HomeView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Test.objects.order_by('-pub_date')


def open_test(request, test_id):
        test_ = get_object_or_404(Test, pk=test_id)
        print(test_)
        open_q = Question.choice_set.get(pk=request.POST['test_id'])
        print(open_q)
        return render(request, 'polls/detail.html', {'test': test_})


# def detail(request, test_id):
#     try:
#         question = Test.objects.get(pk=test_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})
    #def detail(request, question_id):
    #    question = get_object_or_404(Question, pk=question_id)
    #    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):

        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не сделали выбор",
        })
    else:

        resultpoll = models.ResultTest.objects.get(id=question.id)
        resultpoll.balls += selected_choice.votes
        resultpoll.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def profile(request, user_id):
#     try:
#         user_profile = models.Profile.objects.get(user_id=user_id)
#         posts = models.Post.objects.filter(user_id=user_id)
#         return render(request, 'registration/profile.html', {'user': user_profile, 'posts': posts})
#     except (User.DoesNotExist, models.Profile.DoesNotExist):
#         return redirect('home')



