# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=140)
	body =  models.TextField()
	date = models.DateTimeField()
	image = models.ImageField(upload_to="blog/uploads/", blank=True)
	website = models.URLField(blank=True)
	#website = models.URLField(max_length=50, default='')


	#def __unicode__(self): #python2
	def __str__(self): #python3
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	
	def __str__(self):
		return self.name


class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title

		