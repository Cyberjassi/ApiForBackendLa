# Generated by Django 5.0.2 on 2024-04-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_student_otp_digit_student_verify_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='detail',
            field=models.TextField(null=True),
        ),
    ]