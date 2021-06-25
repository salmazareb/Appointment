from django.db import models
import re
import bcrypt 

# Create Model Manger 
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        user_in_db = User.objects.filter(email=postData['email'])
    
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        if len(postData['password']) < 8:
            errors['password'] = "Hey, your password need to have more than 8 characters"
        if postData['password'] != postData['pwd_confirm']:
            errors['password'] = "Passwords must match"


        if user_in_db:
            errors['email'] = "User already exists"
        return errors 

    def login_validator(self, postData ):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            login_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), login_user.password.encode()):
                errors['password'] = "Invalid login"
        else:
            errors['password'] = "Invalid login"
        return errors 

class TaskManager(models.Manager):
    def task_validator(self, postData ):
        errors = {}
        if len(postData['task']) < 8:
            errors['task'] = "Hey, you need to enter more than 8 characters"
        return errors 
        
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Task(models.Model):
    task = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="tasks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()
