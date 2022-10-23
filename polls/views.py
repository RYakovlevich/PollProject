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
        try:
            test_ = Question.objects.filter(testnumb_id=test_id)
        except Test.DoesNotExist:
            raise Http404("Не найден тест")

        # test_ = get_object_or_404(Question, pk=test_id)
        # print('test_', test_[0].id)
        # for i in test_:
        #     y = test_[i].id
        #     print('test_тайп', i)
        #     tj = [].append(y)
        tes = test_.first()

        return render(request, 'polls/detail.html', {'test': tes})


def results(request, test_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'test': question})


def vote(request, test_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(selected_choice)

    except (KeyError, Choice.DoesNotExist):

        return render(request, 'polls/detail.html', {
            'test': question,
            'error_message': "Вы не сделали выбор",
        })
    try:
        res_quest = ResultTest.objects.get(user_id=request.user.id, question_id=question_id)
        res_quest.save()
        print(res_quest, 'res_quest')

    except ResultTest.DoesNotExist:
        res_quest = ResultTest.objects.create(
            user_id=request.user.id,
            question_id=question_id,
            balls=0)
        if selected_choice.answer is True:
            res_quest.balls += 1
            res_quest.save()
    selected_choice.votes += 1
    selected_choice.save()

    print(selected_choice.answer, 'answeeeeeeeeeeeeeeeeeeeeeeeer')

    return HttpResponseRedirect(reverse('polls:results', args=(test_id, question_id,)))


# def profile(request, user_id):
#     try:
#         user_profile = models.Profile.objects.get(user_id=user_id)
#         posts = models.Post.objects.filter(user_id=user_id)
#         return render(request, 'registration/profile.html', {'user': user_profile, 'posts': posts})
#     except (User.DoesNotExist, models.Profile.DoesNotExist):
#         return redirect('home')



