# Generated by Django 3.1.8 on 2021-07-09 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_compare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compare',
            old_name='product',
            new_name='compareproduct',
        ),
    ]
