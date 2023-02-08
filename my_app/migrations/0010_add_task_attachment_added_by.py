# Generated by Django 4.1.4 on 2023-02-08 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0009_sub_space_attachment_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task_attachment',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_auth_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
