# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model): 
	#this line is required to link UserProfile to a User model instance
	user = models.OneToOneField(User)

	#the additionnal attributes we wish to include
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	#override the __unicode__ methos to return out something meaningful
	def __unicode__(self):
		return self.user.username
