# Generated by Django 3.1.3 on 2021-05-30 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210423_1424'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='lastname',
            new_name='last_name',
        ),
    ]