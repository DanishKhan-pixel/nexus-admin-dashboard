# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_investor= models.BooleanField(default=False)
    is_ent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    image=models.ImageField(upload_to='profile',blank=True)
    address=models.CharField(max_length=100,blank=True)
    city=models.CharField(max_length=100,blank=True)
    country=models.CharField(max_length=100,blank=True)
    zip=models.CharField(max_length=100,blank=True)
    bio=models.TextField(blank=True)
    int_date=models.DateTimeField(blank=True,null=True)
    int_link=models.TextField(blank=True)

