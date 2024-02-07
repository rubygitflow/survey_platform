from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *
from survey.services.analytics import Analytics
import environ

env = environ.Env()

def index(request):
    data = {
        "title": "SURVEY-PLATFORM",
        "questionnaires": Questionnaire.objects.filter(exposed=True)
    }
    return render(request, 'survey/index.html', context=data)

def polling(request, queid):
    questionnaire = Questionnaire.objects.filter(pk = queid)
    question = Question.objects.filter(questionnaire_id=queid, initial=True)
    if len(questionnaire) == 0 or len(question) == 0:
        return redirect('home', permanent = False)

    data = {
        "title": "SURVEY",
        "questionnaire": questionnaire[0],
        "question": question[0],
    }
    return render(request, 'survey/questionnaire.html', context=data)

def error_404(request, exception):
   return HttpResponseNotFound(f'<h1>Page not found</h1>')

def poll(request, polid, queid):
    if request.method == 'POST':
        last_question = request.GET.get('last_question')
        last_answer = request.GET.get('last_answer')

        if last_question:
            last_question = int(last_question)

        if last_answer:
            last_answer = int(last_answer)

        question = Question.objects.get(id=queid)
        answers = Answer.objects.filter(question_id=queid)

        if last_question and last_question > 0:
            previous_voting = Poll.objects.filter(
                user_id=env('USER_ID'),
                questionnaire_id=question.questionnaire_id,
                question_id=last_question,
                answer_id=last_answer
            )
            if not bool(previous_voting):
                Poll.objects.create(
                    user_id=env('USER_ID'),
                    questionnaire_id=question.questionnaire_id,
                    question_id=last_question,
                    answer_id=last_answer
                )

        if question.conclusion:
            if last_question and last_question > 0:
                a = Analytics(questionnaire_id=polid)
                analytics_by_questions = a.rating_of_questions(question_id=last_question)
                analytics_by_answers = a.rating_of_answers(question_id=last_question)
            else:
                analytics_by_questions = []
                analytics_by_answers = []
        else:
            analytics_by_questions = []
            analytics_by_answers = []

        data = {
            "is_final": question.conclusion,
            "title": "SURVEY",
            "question": question,
            "answers": answers,
            "analytics_by_questions": analytics_by_questions,
            "analytics_by_answers": analytics_by_answers,
        }
    else:
        data = {
            "is_final": False,
            "title": "SURVEY",
            "question": Question(questionnaire_id=Questionnaire.objects.first().pk, body="Start a new Questionnaire"),
            "answers": [],
            "analytics_by_questions": [],
            "analytics_by_answers": [],
        }

    return render(request, 'survey/poll.html', context=data)

