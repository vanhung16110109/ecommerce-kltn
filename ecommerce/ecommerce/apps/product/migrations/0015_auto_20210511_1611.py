# Generated by Django 3.1.3 on 2021-05-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20210510_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='variant',
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='minamount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=20),
        ),
        migrations.AlterField(
            model_name='variants',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
