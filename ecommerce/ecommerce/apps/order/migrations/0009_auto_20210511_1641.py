# Generated by Django 3.1.3 on 2021-05-11 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20210511_1641'),
        ('order', '0008_auto_20210511_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.variants'),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
