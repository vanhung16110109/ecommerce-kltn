import random
import os
from django.db import models
from apps.product.untils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from django import forms
from django.forms import ModelForm


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
class Category(MPTTModel):
    STATUS = (('TRUE', 'TRUE'),
                ('FALSE', 'FALSE'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    #description = models.CharField(max_length=255)
    #image = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)



class Category_Product_Detail(MPTTModel):
    STATUS = (('TRUE', 'TRUE'),
                ('FALSE', 'FALSE'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    #description = models.CharField(max_length=255)
    #image = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category_Product_Detail)


# Create your models here.
class Product(models.Model):
    STATUS = (('TRUE', 'TRUE'),
                ('FALSE', 'FALSE'))
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    price = models.DecimalField(max_digits=12, decimal_places=3,default=0)
    amount = models.IntegerField()
    minamount = models.IntegerField()
    variant = models.CharField(max_length=10, choices=VARIANTS, default = 'None')
    detail = RichTextUploadingField()
    #Technical specifications
    tespproduct = RichTextUploadingField()			
    slug = models.SlugField(blank=False, null=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    #banner = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    statusdiscount = models.CharField(max_length=10, choices=STATUS)
    pricediscount = models.DecimalField(max_digits=20, decimal_places=3)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description='Image'


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)



class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to=upload_image_path)

    def __str__(self):
        return self.title


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    banner = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=False, null=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


def productpresavereceiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(productpresavereceiver, sender=Banner)



class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null = True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Màu </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null = True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null = True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null = True)
    image_id = models.IntegerField(blank = True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=3,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']