from django.db import models
import re
from datetime import date
class ManageUser(models.Manager):
    def basic_validator(self,postData):
        errors={}
       
        email_re= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
       
        if len(postData['firstname'])<3 : 
            errors['firstname']="at least 2 characters; letters only"
        if len(postData['lastname'])<3:
            errors['lastname']="at least 2 characters; letters only"
        if not email_re.match(postData['email']):
            errors['email']="email invalid pattern or is exist "
        if User.objects.filter(email=postData['email']):
            errors["email"]="the email exist"
        if len(postData['password'])<8 :
            print(postData['password'])
            errors['email']="has to more than 8 characters"
        if  postData['confirmpw'] != postData['password']:
            errors['confirmpw']="both password arenot match"
       
        
        return errors
class ManageBook(models.Manager):
    def basic_validator(self,postData):
        errors={}
       
        if len(postData['title'])<1: 
            errors['title']="Title is required"
        if len(postData['desc'])<5:
            errors['desc']="at least 5 characters for Description"
        return errors
class User(models.Model):
  firstname=models.CharField(max_length=255)
  lastname=models.CharField(max_length=255)
  email=models.CharField(max_length=255)
  password=models.CharField(max_length=255)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects=ManageUser()

class Book(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    uploaded=models.ForeignKey(User,related_name="Books_uploaded",on_delete=models.CASCADE)
    userslike=models.ManyToManyField(User,related_name="Books")
    objects=ManageBook()