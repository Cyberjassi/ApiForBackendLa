# Generated by Django 5.0.2 on 2024-05-06 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_teacher_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentcourseenrollment',
            name='teacher',
        ),
    ]
