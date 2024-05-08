# Create your models here.
from django.db import models
from django.core.validators import RegexValidator
import datetime


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    SSN = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, unique=True)
    authentication_hash = models.CharField(max_length=256)  # validators=['TODO: Add password rules'])

    class Meta:
        app_label = 'utilities_static'

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_ssn = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=14, unique=True)
    company_info = models.TextField()

    class Meta:
        app_label = 'utilities_static'

    def __str__(self) -> str:
        return self.company_name


class Category(models.Model):
    field = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'


class EmploymentType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'


class Status(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'
