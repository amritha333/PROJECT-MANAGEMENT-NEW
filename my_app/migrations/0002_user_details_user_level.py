# Generated by Django 4.1.4 on 2023-01-25 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='user_level',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Normal Staff', 'Normal Staff')], max_length=25, null=True),
        ),
    ]