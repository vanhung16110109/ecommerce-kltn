# Generated by Django 3.1.8 on 2021-07-05 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20210705_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transport_fee',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]