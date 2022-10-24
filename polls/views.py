from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
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
    print(request,test_id,queue)
    print('_______)________________)_____________________)))))))))))))))))))))))))))))))))')
    try:
        question = Question.objects.get(testnumb=test_id, queue=queue)

    except Question.DoesNotExist:
        raise Http404("Не найден вопрос")
        # return render(request, 'polls/result_test.html')
    print(question)
    return render(request, 'polls/detail.html', {'question': question},)


def vote(request, test_id, queue):
    question = get_object_or_404(Question, queue=queue, testnumb_id=test_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(selected_choice)

    except (KeyError, Choice.DoesNotExist):

        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не сделали выбор",
        })
    try:
        res_quest = ResultTest.objects.get(user_id=request.user.id, question_id=question.id)

        print(res_quest, 'res_quest')

    except ResultTest.DoesNotExist:
        res_quest = ResultTest.objects.create(
            user_id=request.user.id,
            question_id=question.id,
            balls=0)
        if selected_choice.answer is True:
            res_quest.balls += 1
            res_quest.save()
    selected_choice.votes += 1
    selected_choice.save()

    print(selected_choice.answer, 'answeeeeeeeeeeeeeeeeeeeeeeeer')

    return render(request, 'polls/results.html', {'question': question})


