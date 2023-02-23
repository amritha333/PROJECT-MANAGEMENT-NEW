# Generated by Django 4.1.4 on 2023-02-20 07:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0011_add_task_checklist_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task_master',
            name='invite_user_auth_id',
            field=models.ManyToManyField(related_name='add_task_auth_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='add_task_master',
            name='invite_user_details_id',
            field=models.ManyToManyField(related_name='add_task_user_id', to='my_app.user_details'),
        ),
    ]