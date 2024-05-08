from django.contrib import admin
from utilities_static.models import *
from django.apps import apps
from django.contrib.admin.exceptions import AlreadyRegistered

model_classes = [cls for name, cls in vars().items() if isinstance(cls, type) and issubclass(cls, models.Model)]

for model_class in model_classes:
    try:
        admin.site.register(model_class)
    except AlreadyRegistered:
        print(f"{model_class.__name__} is already registered.")
