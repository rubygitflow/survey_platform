from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from survey.services.analytics import Analytics
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *
from .services.trie import Trie

# https://docs.djangoproject.com/en/5.0/topics/auth/default/#authentication-in-web-requests

def index(request):
    data = {
        "title": "SURVEY-PLATFORM",
        "questionnaires": Questionnaire.objects.filter(exposed=True)
    }
    return render(request, 'survey/index.html', context=data)

def polling(request, queid):
    if not request.user.is_authenticated:
        return redirect('login')

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
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        last_question = request.GET.get('last_question')
        last_answer = request.GET.get('last_answer')

        if last_question:
            last_question = int(last_question)

        if last_answer:
            last_answer = int(last_answer)

        # to verify honesty
        if Trie().is_cheating(
            user_id=request.user.id,
            questionnaire_id=polid,
            question_id=last_question,
            for_answer_id=last_answer
        ):
            return redirect('fraud')


        # data on the current page
        question = Question.objects.get(id=queid)
        answers = Answer.objects.filter(question_id=queid)

        # voted – to block answers on the curent page
        ids = answers.values_list('id', flat=True)
        voted = bool(
          Poll.objects.filter(
              user_id=request.user.id,
              questionnaire_id=polid,
              question_id=queid,
              answer_id__in=ids
          )
        )

        # Poll.objects.create – to add a previous answer to the survey results
        if last_question and last_question > 0:
            previous_voting = Poll.objects.filter(
                user_id=request.user.id,
                questionnaire_id=question.questionnaire_id,
                question_id=last_question,
                answer_id=last_answer
            )
            if not bool(previous_voting):
                Poll.objects.create(
                    user_id=request.user.id,
                    questionnaire_id=question.questionnaire_id,
                    question_id=last_question,
                    answer_id=last_answer
                )

        # analytics_by_questions, analytics_by_answers – to generate an analytical report
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
            "voted": voted,
        }
    else:
        data = {
            "is_final": False,
            "title": "SURVEY",
            "question": Question(questionnaire_id=Questionnaire.objects.first().pk, body="Start a new Questionnaire"),
            "answers": [],
            "analytics_by_questions": [],
            "analytics_by_answers": [],
            "voted": False,
        }

    return render(request, 'survey/poll.html', context=data)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'survey/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sign up")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'survey/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sign in")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def fraud(request):
    data = {
        "title": "SURVEY-PLATFORM",
    }
    return render(request, 'survey/fraud.html', context=data)
