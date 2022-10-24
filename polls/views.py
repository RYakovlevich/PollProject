from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Question, Choice, ResultTest, Test
from django.views.generic import ListView


class HomeView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Test.objects.order_by('-pub_date')


def open_test(request, test_id):

    try:
        question = Question.objects.filter(testnumb=test_id).order_by('queue').first()
    except Test.DoesNotExist:
        raise Http404("Не найден тест")

    return render(request, 'polls/detail.html', {'question': question},)


def next_question(request, test_id, queue):

    try:
        question = Question.objects.get(testnumb=test_id, queue=queue)

    except Question.DoesNotExist:
        q = ResultTest.objects.filter(test_done_id=test_id, user_id=request.user.id).all()
        sum_true =q.filter(balls=1).count()
        sum = q.count()
        persent = sum_true/sum*100
        context = {'q': q,
                   'sumtrue': sum_true,
                   'sum': sum,
                   'persent': persent
                   }

        return render(request, 'polls/resulttest.html', context)
    return render(request, 'polls/detail.html', {'question': question},)


def vote(request, test_id, queue):
    question = get_object_or_404(Question, queue=queue, testnumb_id=test_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):

        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не сделали выбор",
        })
    try:
        res_quest = ResultTest.objects.get(user_id=request.user.id, question_id=question.id)
    except ResultTest.DoesNotExist:
        res_quest = ResultTest.objects.create(
            user_id=request.user.id,
            question_id=question.id,
            test_done_id=test_id,
            balls=0)
        if selected_choice.answer is True:
            res_quest.balls += 1
            res_quest.save()
    selected_choice.votes += 1
    selected_choice.save()

    return render(request, 'polls/results.html', {'question': question})
