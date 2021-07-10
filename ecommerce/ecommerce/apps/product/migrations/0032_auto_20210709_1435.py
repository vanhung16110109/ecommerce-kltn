# Generated by Django 3.1.8 on 2021-07-09 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20210709_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_backcam',
            new_name='backcam',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_battery',
            new_name='battery',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_connection',
            new_name='connection',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_cpu',
            new_name='cpu',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_frontcam',
            new_name='frontcam',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_general',
            new_name='general',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_memory',
            new_name='memory',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproduct_screen',
            new_name='screen',
        ),
        migrations.RenameField(
            model_name='compare',
            old_name='detailsproductc_utils',
            new_name='utils',
        ),
    ]