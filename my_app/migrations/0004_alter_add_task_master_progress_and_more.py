# Generated by Django 4.1.4 on 2023-01-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_sub_tasks_dynamic_status_sub_tasks_group_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_task_master',
            name='progress',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In progress', 'In progress'), ('Completed', 'Completed')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sub_space_master',
            name='progress',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In progress', 'In progress'), ('Completed', 'Completed')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='sub_tasks',
            name='progress',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('In progress', 'In progress'), ('Completed', 'Completed')], max_length=50, null=True),
        ),
    ]
