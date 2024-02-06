from django.contrib import admin
from .models import Questionnaire, Question, Answer, Poll

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_add_permission
# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields

class PollAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class QuestionnaireAdmin(admin.ModelAdmin):
    search_fields = ['caption']

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['body']

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['body']

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Poll, PollAdmin)
