from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Student(models.Model):
    studentname = models.CharField(max_length=150, unique=True, null=False, blank=False)
    roll = models.CharField(max_length=150, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False)
    mobile = models.CharField(max_length=15, null=False, blank=False, unique=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=105, null=False, blank=False)
    classes = models.CharField(max_length=15)
    blood = models.CharField(max_length=15)
    college = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=100,default="Waiting")
    qr = models.ImageField(upload_to="qrcodes/", null=True, blank=True)

class Present(models.Model):
    date = models.DateField(null=True, blank=True)
    classes = models.CharField(max_length=15)
    studentname = models.CharField(max_length=150, null=False, blank=False)
    roll = models.CharField(max_length=150, null=False, blank=False)
    college = models.CharField(max_length=150, null=False, blank=False)
    mobile = models.CharField(max_length=15, null=False, blank=False)