# Generated by Django 5.0.2 on 2024-04-16 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_attempquiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempquiz',
            name='right_ans',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
