from django.db import models

# Create your models here.
from django.db import models as django_models
from django.core.validators import RegexValidator

from utilities_static.models import User, Company, Category, EmploymentType, Status
import datetime


# Create your models here.

class Recruiter(django_models.Model):
    user = django_models.OneToOneField(User, on_delete=django_models.CASCADE, primary_key=True)
    company_ssn = django_models.CharField(max_length=10)

    class Meta:
        app_label = 'company'


class JobListing(django_models.Model):
    id = django_models.AutoField(primary_key=True)
    company = django_models.ForeignKey(Company, on_delete=django_models.CASCADE)
    salary_low = django_models.IntegerField()
    salary_high = django_models.IntegerField()
    recruiter = django_models.ForeignKey(Recruiter, on_delete=django_models.CASCADE)
    category = django_models.ForeignKey(Category, on_delete=django_models.CASCADE)
    employment_type = django_models.ForeignKey(EmploymentType, on_delete=django_models.CASCADE)

    class Meta:
        app_label = 'company'


class Application(django_models.Model):
    user = django_models.OneToOneField(User, on_delete=django_models.CASCADE)
    date = django_models.DateField(default=datetime.date.today)
    listing = django_models.OneToOneField(JobListing, on_delete=django_models.CASCADE)
    django_models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')
    status = django_models.OneToOneField(Status, on_delete=django_models.CASCADE)

    class Meta:
        app_label = 'company'

