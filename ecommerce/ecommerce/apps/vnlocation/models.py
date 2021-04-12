from django.db import models
from apps.vnlocation import querydb
import sqlite3

# a = querydb.show_province()
# for i in a:
# 	print(i[0])


# Create your models here.
class Province(models.Model):
	provinceid = models.CharField(blank=True, max_length=10)
	name = models.CharField(blank=True, max_length=50)


	def __str__(self):
		return self.provinceid

	def __unicode__(self):
		return self.provinceid














