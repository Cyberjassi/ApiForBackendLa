# Generated by Django 5.0.2 on 2024-04-16 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_quiz_coursequiz_quizquestions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizquestions',
            old_name='questions',
            new_name='question',
        ),
    ]