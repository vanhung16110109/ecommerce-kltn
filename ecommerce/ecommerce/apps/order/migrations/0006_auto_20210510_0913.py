# Generated by Django 3.1.8 on 2021-05-10 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210510_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcart',
            name='variant',
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='quantity',
            field=models.DecimalField(decimal_places=0, max_digits=20),
        ),
    ]
