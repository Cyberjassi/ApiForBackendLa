# Generated by Django 5.0.2 on 2024-04-16 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_coursequiz_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizquestions',
            old_name='question',
            new_name='questions',
        ),
    ]
