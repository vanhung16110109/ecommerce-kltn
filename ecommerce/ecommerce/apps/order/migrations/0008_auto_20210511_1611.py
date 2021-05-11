# Generated by Django 3.1.3 on 2021-05-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210510_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variant',
        ),
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
