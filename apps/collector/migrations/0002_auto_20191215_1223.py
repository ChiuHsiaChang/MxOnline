# Generated by Django 2.2 on 2019-12-15 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='content_id',
            new_name='course_id',
        ),
    ]
