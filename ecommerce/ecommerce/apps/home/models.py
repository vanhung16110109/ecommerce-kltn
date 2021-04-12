import os
import random

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


# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=255)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at =  models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=30)
    note = models.CharField(blank=True, max_length=100)
    create_at =  models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.title


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name'      : TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'email'     : TextInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'subject'   : TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message'   : Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows':'10'}),
        }


# from django.db import models
# from .form import PROVINCEID, PROVINCE, DISTRICTID, DISTRICT

# # Create your models here.
# class Province(models.Model):
# 	provinceid = models.CharField(blank=True, max_length=10, choices=PROVINCEID)
# 	name = models.CharField(blank=True, max_length=50, choices=PROVINCE)

# 	def __str__(self):
# 		return self.provinceid

# 	def __unicode__(self):
# 		return self.provinceid


# class District(models.Model): 
# 	districtid = models.CharField(blank=True, max_length=10, choices=DISTRICTID)
# 	name = models.CharField(blank=True, max_length=50, choices=DISTRICT)
# 	provinceid = models.ForeignKey(Province,on_delete=models.CASCADE)


