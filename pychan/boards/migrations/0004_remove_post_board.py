# Generated by Django 3.2.8 on 2021-12-11 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20211110_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='board',
        ),
    ]
