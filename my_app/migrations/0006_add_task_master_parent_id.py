# Generated by Django 4.1.4 on 2023-02-06 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_tags_name_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task_master',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_task', to='my_app.add_task_master'),
        ),
    ]
