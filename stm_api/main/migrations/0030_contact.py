# Generated by Django 5.0.2 on 2024-04-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('query_txt', models.TextField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '17. Contact Queries',
            },
        ),
    ]
