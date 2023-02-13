# Generated by Django 4.1.4 on 2023-02-13 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_space_master',
            name='tag_id',
            field=models.ManyToManyField(related_name='sub_space_tag', to='my_app.tags_name_master'),
        ),
        migrations.AlterField(
            model_name='role_mapping',
            name='navbar_name',
            field=models.CharField(choices=[('Company', 'Company'), ('User', 'User'), ('Role', 'Role'), ('Team member', 'Team member'), ('Tags', 'Tags'), ('Status', 'Status')], max_length=50, null=True),
        ),
    ]
