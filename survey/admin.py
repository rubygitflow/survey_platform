""" Admin panel configuration """
# pylint: disable=missing-class-docstring

from django.contrib import admin
from .models import Questionnaire, Question, Answer, Poll

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_add_permission
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display

class PollAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('id', 'questionnaire_id', 'user_id', 'question_id', 'answer_id')

class QuestionnaireAdmin(admin.ModelAdmin):
    search_fields = ['caption']
    list_display = ('id', 'caption', 'exposed')


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['body']
    list_display = ('id', 'questionnaire_id', 'body', 'conclusion', 'initial')

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['body']
    list_display = ('id', 'question_id', 'body', 'next_question_id')

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Poll, PollAdmin)
