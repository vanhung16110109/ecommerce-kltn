# Generated by Django 3.1.8 on 2021-07-09 06:56

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20210709_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailsproduct_screen', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_backcam', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_frontcam', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_cpu', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_memory', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_connection', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_battery', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproductc_utils', ckeditor_uploader.fields.RichTextUploadingField()),
                ('detailsproduct_general', ckeditor_uploader.fields.RichTextUploadingField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]