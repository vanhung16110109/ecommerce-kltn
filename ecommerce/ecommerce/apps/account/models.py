import os
import random
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from apps.home.form import PROVINCE


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,9999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "users/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(blank=True, max_length=50)
    firstname = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=50, choices=PROVINCE)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to=upload_image_path)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.city

    def user_name(self):
        return self.user.first_name + '' + self.user.last_name + '[' + self.user.username + ']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
