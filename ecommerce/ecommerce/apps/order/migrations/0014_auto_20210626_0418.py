# Generated by Django 3.1.8 on 2021-06-25 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_order_status_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_pay',
            field=models.CharField(choices=[('Chưa thanh toán', 'Chưa thanh toán'), ('Đã thanh toán', 'Đã thanh toán')], default='Chưa thanh toán', max_length=50),
        ),
    ]
