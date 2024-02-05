from django.contrib import admin
from .models import Questionnaire, Question, Answer, Poll

class PollAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Poll, PollAdmin)
