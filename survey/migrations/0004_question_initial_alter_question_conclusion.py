# Generated by Django 5.0.1 on 2024-02-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_poll'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='initial',
            field=models.BooleanField(default=False, verbose_name='Начало опроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='conclusion',
            field=models.BooleanField(default=False, verbose_name='Окончание опроса'),
        ),
    ]
