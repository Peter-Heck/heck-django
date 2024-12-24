from django.db import models
import os
from HeckWebsite import settings
from django.contrib.auth.models import User as DjangoUser
from datetime import datetime

# This number will ensure that new users have different usernames when the default is made
counter = 0

def update_counter():
    global counter
    counter = counter + 1

# Create your models here.
class User(models.Model):
    global counter
    default_name = 'unknown' + str(counter)
    update_counter()
    name = models.CharField(max_length=80, default=default_name)
    profilePic = models.ImageField(upload_to='profilePics', default='profilePics/blank-profile.png')
    bio = models.CharField(max_length=250, default='Bio')
    
    def __str__(self):
        return (f"ID: {self.id}, Name: {self.name}, Bio: {self.bio}, Picture Used: {self.profilePic}")

class UserProfile(models.Model):
    user = models.ForeignKey(DjangoUser, default=1, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=80, unique=True, blank=True, null=True)
    profilePic = models.ImageField(upload_to=os.path.join('profilePics', datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')), blank=True, null=True, unique=False, default='profilePics/blank-profile.png')
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return (f"ID: {self.id}, Name: {self.name}, Bio: {self.bio}, Picture Used: {self.profilePic}, User ID: {self.user.id}")
    
    
class Post(models.Model):
    author = models.ForeignKey(DjangoUser, default=1, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    title = models.CharField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=os.path.join('postPics', datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'), datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S'), datetime.now().strftime('%f')), null=True, blank=True)
    time = datetime.now()
    post_date = models.DateTimeField(default=time)
    updated_on = models.DateTimeField(default=time)
    
    def __str__(self):
        return (f"ID: {self.id}, Author ID: {self.author.id}, Title: {self.title}, Content: {self.body}, Upload Date: {self.post_date}")

def upload_to_date_directory(instance, filename):
    now = datetime.now()
    print()
    return os.path.join('postPics', now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'))

# class PostImages(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
    