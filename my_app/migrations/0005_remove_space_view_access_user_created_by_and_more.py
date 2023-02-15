# Generated by Django 4.1.4 on 2023-02-15 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_project_user_access_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='space_view_access_user',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='space_view_access_user',
            name='space_id',
        ),
        migrations.RemoveField(
            model_name='space_view_access_user',
            name='space_view_auth_id',
        ),
        migrations.RemoveField(
            model_name='space_view_access_user',
            name='space_view_user_details',
        ),
        migrations.RemoveField(
            model_name='space_view_access_user',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='space_master',
            name='manager_auth',
        ),
        migrations.DeleteModel(
            name='space_access_permission_user',
        ),
        migrations.DeleteModel(
            name='space_view_access_user',
        ),
    ]