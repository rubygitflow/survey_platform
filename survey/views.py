""" Application Views """
# pylint: disable=missing-class-docstring

from django.utils.translation import gettext as _
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from survey.services.analytics import Analytics
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import RegisterUserForm, LoginUserForm
from .models import Questionnaire, Question, Answer, Poll
from .utils import DataMixin
from .services.trie import Trie

# https://docs.djangoproject.com/en/5.0/topics/auth/default/#authentication-in-web-requests


def fullname():
    """ Application full logo """
    return "SURVEY-PLATFORM"

def shortname():
    """ Application short logo """
    return "SURVEY"

def analyst():
    """ Headings of the Analytical table """
    return {
        'question_number': _('Question number'),
        'answer_number': _('Answer number'),
        'question_text': _('Question text'),
        'answer_text': _('Answer text'),
        'number_voted_users': _('Number of users who voted'),
        'pct_of_voters': _("% of voters"),
        'question_rating': _('Question rating'),
        'answer_rating': _('Answer rating'),
        'survey_results_by_questions': _('SURVEY RESULTS BY QUESTIONS'),
        'survey_results_by_answers': _('SURVEY RESULTS BY ANSWERS'),
        'total_number_of_survey_participants': _('Total number of survey participants'),
    }

def navbar():
    """ Headings of the Navbar controls """
    return {
        'home': _('Home'),
        'about_author': _('About the author'),
        'change_lang': _('Change'),
        'sign_out': _('Sign out'),
        'sign_in': _('Sign in'),
        'sign_up': _('Sign up'),
    }

def index_labels():
    """ The title of the survey list """
    return {
        'choose_survey': _('Choose a survey topic to participate in the study'),
    }

def fraud_labels():
    """ The title of the fraud page """
    return {
        'fraud_detected': _('Fraud is detected. It is forbidden to change answers'),
    }

def nav_controls():
    """ Navigation control headers """
    return {
        'start': _('Start'),
        'back_to_polls': _('Back to the list of polls'),
    }

def poll_labels():
    """ Warning during survey """
    return {
        'warning': _('Warning!'),
        'choose_carefully': _(
            'Choose the answer carefully. It will no longer be possible to change it.'
        ),
    }

def questionnaire_labels():
    """ Exceptional warning before survey """
    return {
        'completed_survey': _('You have already completed the survey'),
    }

def index(request):
    """ Index page """
    data = {
        "title": fullname(),
        "questionnaires": Questionnaire.objects.filter(exposed=True),
        'redirect_to': request.path,
    } | navbar() | index_labels()
    return render(request, 'survey/index.html', context=data)

@login_required(login_url='login')
def polling(request, queid):
    """ Questionnaire page """
    questionnaire = Questionnaire.objects.filter(pk = queid)
    title = {
        "title": shortname(),
        'redirect_to': request.path,
    } | analyst() | navbar() | nav_controls() | questionnaire_labels()
    if request.user.is_staff:
        a = Analytics(questionnaire_id=queid)
        data = {
            "user_is_staff": request.user.is_staff,
            "questionnaire": questionnaire[0],
            "analytics_by_questions": a.questions_rating(),
            "analytics_by_answers": a.answers_rating(),
            "count_of_vouted_users": a.count_of_vouted_users(),
        }
    else:
        question = Question.objects.filter(questionnaire_id=queid, initial=True)
        if len(questionnaire) == 0 or len(question) == 0:
            return redirect('home', permanent = False)

        completed = bool(
          Poll.objects.filter(
              user_id=request.user.id,
              questionnaire_id=queid,
              question_id=question[0].pk,
          )
        )
        data = {
            "user_is_staff": request.user.is_staff,
            "questionnaire": questionnaire[0],
            "question": question[0],
            "completed": completed,
        }
    return render(request, 'survey/questionnaire.html', context=data | title)

def error_404(request, _exception):
    """ The page with the 404 error """
    return HttpResponseNotFound(f'<h1>Page not found</h1>')

@login_required(login_url='login')
def poll(request, polid, queid):
    """ Survey page """
    total_count_of_users = 0
    title = {
        "title": shortname(),
        "skip_language_selection": True,
        'redirect_to': request.path,
    } | analyst() | navbar() | poll_labels() | nav_controls()

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
                total_count_of_users = a.count_of_vouted_users()
            else:
                analytics_by_questions = []
                analytics_by_answers = []
        else:
            analytics_by_questions = []
            analytics_by_answers = []

        data = {
            "is_final": question.conclusion,
            "question": question,
            "questionnaire": question.questionnaire,
            "answers": answers,
            "analytics_by_questions": analytics_by_questions,
            "analytics_by_answers": analytics_by_answers,
            "count_of_vouted_users": total_count_of_users,
            "voted": voted,
        }
    else:
        question = Question(
            questionnaire_id=Questionnaire.objects.first().pk,
            body="Start a new Questionnaire")
        data = {
            "is_final": False,
            "question": question,
            "questionnaire": question.questionnaire,
            "answers": [],
            "analytics_by_questions": [],
            "analytics_by_answers": [],
            "count_of_vouted_users": total_count_of_users,
            "voted": False,
        }

    return render(request, 'survey/poll.html', context=data | title)

class RegisterUser(DataMixin, CreateView):
    """ Registration form page """
    form_class = RegisterUserForm
    template_name = 'survey/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, _object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=fullname()) | navbar()
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    """ Login form page """
    form_class = LoginUserForm
    template_name = 'survey/login.html'

    def get_context_data(self, *, _object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=fullname()) | navbar()
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    """ Logout endpoint """
    logout(request)
    return redirect('login')

def fraud(request):
    """ Fraud reporting page """
    title = {
        "title": fullname(),
        'redirect_to': request.path,
    } | navbar() | fraud_labels()
    return render(request, 'survey/fraud.html', context=title)
