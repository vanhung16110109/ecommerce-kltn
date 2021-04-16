import os
import random
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,9999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "users/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

CITY = [
    ('An Giang', 'An Giang'), ('Bà Rịa-Vũng Tàu', 'Bà Rịa-Vũng Tàu'), ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Kạn', 'Bắc Kạn'), ('Bắc Giang', 'Bắc Giang'), ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),('Bình Dương', 'Bình Dương'),('Bình Định', 'Bình Định'),
    ('Bình Phước', 'Bình Phước'),('Bình Thuận', 'Bình Thuận'),('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),('Cần Thơ (TP)', 'Cần Thơ (TP)'),('Đà Nẵng (TP)', 'Đà Nẵng (TP)'),
    ('Đắk Lắk', 'Đắk Lắk'),('Đắk Nông', 'Đắk Nông'),('Điện Biên','Điện Biên'),
    ('Đồng Nai','Đồng Nai'),('Đồng Tháp','Đồng Tháp'),('Gia Lai','Gia Lai'),
    ('Hà Giang', 'Hà Giang'),('Hà Nam', 'Hà Nam'),('Hà Nội (TP)', 'Hà Nội (TP)'),
    ('Hà Tây', 'Hà Tây'),('Hà Tĩnh','Hà Tĩnh'),('Hải Dương','Hải Dương'),
    ('Hải Phòng (TP)', 'Hải Phòng (TP)'),('Hòa Bình', 'Hòa Bình'),('Hồ Chí Minh (TP)', 'Hồ Chí Minh (TP)'),
    ('Hậu Giang', 'Hậu Giang'),('Hưng Yên', 'Hưng Yên'),('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),('Kon Tum', 'Kon Tum'),('Lai Châu', 'Lai Châu'),
    ('Lào Cai', 'Lào Cai'),('Lạng Sơn', 'Lạng Sơn'),('Lâm Đồng', 'Lâm Đồng'),
    ('Long An', 'Long An'),('Nam Định', 'Nam Định'),('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),('Ninh Thuận', 'Ninh Thuận'),('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),('Quảng Bình', 'Quảng Bình'),('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),('Quảng Ninh', 'Quảng Ninh'),('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),('Sơn La', 'Sơn La'),('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),('Thái Nguyên', 'Thái Nguyên'),('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên – Huế', 'Thừa Thiên – Huế'),('Tiền Giang', 'Tiền Giang'),('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),('Vĩnh Long', 'Vĩnh Long'),('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
]


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(blank=True, max_length=20)
    lastname = models.CharField(blank=True, max_length=20)
    email = models.EmailField(blank=True, max_length=50)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=50, choices=CITY)
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

