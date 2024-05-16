from django.db import models


class Category(models.Model):
    field = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'

    def __str__(self) -> str:
        return self.field


class EmploymentType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'

    def __str__(self) -> str:
        return self.type


class Status(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        app_label = 'utilities_static'

    def __str__(self) -> str:
        return self.type
