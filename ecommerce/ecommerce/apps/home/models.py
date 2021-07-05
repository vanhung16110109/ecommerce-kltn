import os
import random
from apps.home.vnlocation import CITY, DISTRICT
from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from ckeditor_uploader.fields import RichTextUploadingField

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,9999999999)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class StoreAddress(models.Model):
	title = models.CharField(blank=True, max_length=50)
	ShopID_GHN = models.IntegerField()
	city = models.CharField(blank=True, max_length=50, choices=CITY)
	district = models.CharField(blank=True, max_length=50, choices=DISTRICT)
	insurance_value = models.IntegerField()
	length = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()
	weight = models.IntegerField()


	def __str__(self):
		return self.title

