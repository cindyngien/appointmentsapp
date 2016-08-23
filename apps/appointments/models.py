from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta, date, time
from time import strftime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, data):
        error = []
        bday = data['birthday']
        todaydate = strftime("%Y-%m-%d")
            #index 1 of the innerlist, retrieve in views side
        if len(data["name"]) < 3 or any(char.isdigit() for char in data["name"]):
            error.append('Name must be at least 2 characters and contain no numbers')
        if not EMAIL_REGEX.match(data['email']):
            error.append('Incorrect email')
        if len(data["password"]) < 8:
            error.append('Incorrect password length')
        if bday == "":
            error.append('Birthday cannot be blank!')
        if bday > todaydate:
            error.append('Birthday cannot be a future date')

        user = self.filter(email = data['email']) #check if false

        if user:
            error.append('email taken')
        if data['password'] != data['password_confirm']:
            error.append('please match your passwords')
        if error:
            return (False, error)

        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = self.create(name = data["name"],email = data["email"],birthday=data['birthday'], password = hashed)
        return (True, user)

    def login(self, data):
        error = []
        user = self.filter(email=data['email'])
        if user:
            if bcrypt.hashpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
                return (True, user[0])
        error.append("Invalid credentials, please try again")
        return (False, error)

class AppManager(models.Manager):
    def create_app(self, data, user_id):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H=%M-%S")

        if data['date'] == "":
            errors.append("Date cannot be blank")
        if data['date'] < today:
            errors.append("Enter a valid date")
        if data['time'] == "":
            errors.append("Time cannot be blank")
        if data['date'] == today and data['time'] < now:
            errors.append("Please enter a valid time")
        if len(data['task']) <1:
            errors.append("Task cannot be blank")
        if errors:
            return(False, errors)
        else:
            MyApp.objects.create(myuser=User.objects.get(id=user_id),my_task=data['task'],my_date=data['date'],my_time=data['time'],my_status='Pending')
            return(True, data)

    def edit_app(self, data):
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H=%M-%S")

        if data['date'] == "":
            errors.append("Date cannot be blank")
        if data['date'] < today:
            errors.append("Enter a valid date")
        if data['time'] == "":
            errors.append("Time cannot be blank")
        if data['date'] == today and data['time'] < now:
            errors.append("Please enter a valid time")
        if len(data['task']) <1:
            errors.append("Task cannot be blank")
        if errors:
            return (True, errors)
        else:
            errors.append('Invalid info, try again!')
            return (False, data)

class MyApp(models.Model):
    my_task = models.CharField(max_length=45)
    my_date = models.DateField()
    my_time = models.TimeField()
    myuser = models.ForeignKey('User', related_name="myuser")
    my_status = models.TextField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppManager()

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField()
    birthday = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
