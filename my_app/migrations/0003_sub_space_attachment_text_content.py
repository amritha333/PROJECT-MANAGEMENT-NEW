# Generated by Django 4.1.4 on 2023-02-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_sub_space_master_tag_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_space_attachment',
            name='text_content',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
