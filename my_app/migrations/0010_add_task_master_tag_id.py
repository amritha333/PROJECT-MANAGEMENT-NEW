# Generated by Django 4.1.4 on 2023-02-16 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0009_add_task_attachment_text_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_task_master',
            name='tag_id',
            field=models.ManyToManyField(related_name='Add_task_master_tag', to='my_app.tags_name_master'),
        ),
    ]
