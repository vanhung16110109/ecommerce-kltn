from django.db import models
from .form import PROVINCEID, PROVINCE, DISTRICTID, DISTRICT

# Create your models here.
class Province(models.Model):
	provinceid = models.CharField(blank=True, max_length=10, choices=PROVINCEID)
	name = models.CharField(blank=True, max_length=50, choices=PROVINCE)

	def __str__(self):
		return self.provinceid

	def __unicode__(self):
		return self.provinceid


class District(models.Model): 
	districtid = models.CharField(blank=True, max_length=10, choices=DISTRICTID)
	name = models.CharField(blank=True, max_length=50, choices=DISTRICT)
	provinceid = models.ForeignKey(Province,on_delete=models.CASCADE)


