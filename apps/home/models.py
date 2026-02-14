# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from apps.authentication.models import User
from django.utils import timezone
# Create your models here.

class Bussiness(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    stocks_qty = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PriceHistory(models.Model):
    bussiness = models.ForeignKey(Bussiness, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bussiness.name

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Bussiness, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    status = models.CharField(max_length=100, default='2')
    description = models.TextField(default='')
    link = models.CharField(max_length=100,default='https://www.google.com')
    paid= models.CharField(max_length=100,default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock: {self.user} - {self.symbol}"

class Listings(models.Model):
    ticker = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ticker
    

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default="pro_pic.png", null=True, blank=True)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UserPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={
            'pk': self.pk
    })

    # Use this method as a property 
    @property
    def answer_count(self):
        return Answer.objects.filter(user_post=self).count()
    
    # Use this method as a property 
    @property
    def topic_view_count(self):
        return TopicView.objects.filter(user_post=self).count()

class Answer(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvotes')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvotes')

    def __str__(self):
        return self.user_post.title
    
    @property
    def upvotes_count(self):
        return Answer.objects.filter(user=self).count()

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(default="header.jpg", null=True, blank=True)

    def __str__(self):
        return self.title


class TopicView(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user_post.title

    