from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *

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
  return HttpResponse(f'<h1>Голосование по опроснику</h1><p>{polid}</p><p>{queid}</p>')
