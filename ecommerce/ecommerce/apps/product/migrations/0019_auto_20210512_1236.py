# Generated by Django 3.1.3 on 2021-05-12 05:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_detailsproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detailsproduct',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=2),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DetailsProduct',
        ),
    ]
