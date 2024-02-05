from django.db import models

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
