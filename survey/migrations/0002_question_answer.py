# Generated by Django 5.0.1 on 2024-02-05 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Текст вопроса')),
                ('conclusion', models.BooleanField(default=False, verbose_name='Окончание опроса ')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='survey.questionnaire', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Текст ответа')),
                ('next_question', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='next_questions', to='survey.question', verbose_name='Следующий вопрос')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='questions', to='survey.question', verbose_name='Текущий вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'db_table': 'answers',
            },
        ),
    ]
