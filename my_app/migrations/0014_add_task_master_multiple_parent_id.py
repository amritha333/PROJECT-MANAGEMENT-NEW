# Generated by Django 4.1.4 on 2023-02-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0013_delete_add_task_access_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task_master',
            name='multiple_parent_id',
            field=models.ManyToManyField(blank=True, to='my_app.add_task_master'),
        ),
    ]