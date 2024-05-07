
# Create your models here.
from django.db import models as django_models
from django.core.validators import RegexValidator


# Create your models here.
class User(django_models.Model):
    id = django_models.AutoField(primary_key=True)
    SSN = django_models.CharField(max_length=11, unique=True,
                           validators=[RegexValidator(r'^\d{3}-\d{2}-\d{4}$', 'Enter a valid SSN.')])
    name = django_models.CharField(max_length=100)
    email = django_models.EmailField(unique=True)
    phone_number = django_models.CharField(max_length=14, unique=True)
    authentication_hash = django_models.CharField(max_length=256, unique=True)  # validators=['TODO: Add password rules'])

    class Meta:
        app_label = 'SalarySleuth'


class Company(django_models.Model):
    company_name = django_models.CharField(max_length=100)
    company_ssn = django_models.CharField(max_length=10)
    phone_number = django_models.CharField(max_length=14, unique=True)
    company_info = django_models.TextField()

    class Meta:
        app_label = 'SalarySleuth'


class Category(django_models.Model):
    field = django_models.CharField(max_length=100)


class EmploymentType(django_models.Model):
    type = django_models.CharField(max_length=100)


class Status(django_models.Model):
    type = django_models.CharField(max_length=100)
