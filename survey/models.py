""" Application Models """

from django.db import models
from django.contrib.auth import get_user_model

# https://docs.djangoproject.com/en/5.0/topics/db/models/
# https://docs.djangoproject.com/en/5.0/ref/models/fields/#model-field-types

class Questionnaire(models.Model):
    """Опросник"""

    class Meta:
        db_table = "questionnaires"
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"

    caption = models.CharField(
      verbose_name="Заголовок",
      max_length=255,
    )
    description = models.TextField(
      verbose_name="Описание",
      blank=True,
      null=True,
    )
    exposed = models.BooleanField(
      verbose_name="Выставленный",
      default=False,
    )
    created_at = models.DateTimeField(
      verbose_name="Создано",
      auto_now_add=True,
    )

    def __str__(self):
        return self.caption

class Question(models.Model):
    """Вопрос"""

    class Meta:
        db_table = "questions"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    questionnaire = models.ForeignKey(
      Questionnaire,
      verbose_name="Опрос",
      on_delete=models.RESTRICT,
    )
    body = models.TextField(
      verbose_name="Текст вопроса",
    )
    conclusion = models.BooleanField(
      verbose_name="Окончание опроса",
      default=False,
    )
    initial = models.BooleanField(
      verbose_name="Начало опроса",
      default=False,
    )

    def __str__(self):
        return self.body[ : 25 ]


class Answer(models.Model):
    """Ответ"""

    class Meta:
        db_table = "answers"
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    question = models.ForeignKey(
      Question,
      verbose_name="Текущий вопрос",
      on_delete=models.RESTRICT,
      related_name='questions',
    )
    body = models.TextField(
      verbose_name="Текст ответа",
    )
    next_question = models.ForeignKey(
      Question,
      verbose_name="Следующий вопрос",
      on_delete=models.RESTRICT,
      related_name='next_questions',
    )

    def __str__(self):
        return self.body[ : 25 ]

class Poll(models.Model):
    """результаты опроса"""

    class Meta:
        db_table = "polls"
        verbose_name = "Результат опроса"
        verbose_name_plural = "Результаты опроса"


    user = models.ForeignKey(
      get_user_model(),
      verbose_name="Пользователь",
      on_delete=models.CASCADE
    )
    questionnaire = models.ForeignKey(
      Questionnaire,
      verbose_name="Пройденный опрос",
      on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
      Question,
      verbose_name="Полученный вопрос",
      on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
      Answer,
      verbose_name="Выбранный ответ",
      on_delete=models.CASCADE,
      null=True,
    )

    def __str__(self):
        # pylint: disable=E1101
        return(f"{self.user.username}."
               f"{self.questionnaire.pk}."
               f"{self.question.pk}."
               f"{'' if self.answer is None else self.answer.pk}")
        # pylint: enable=E1101
