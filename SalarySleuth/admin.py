from django.contrib import admin
from SalarySleuth.models import *

# Get all model classes from the models module
model_classes = [cls for name, cls in vars().items() if isinstance(cls, type)]

# Register each model class with the admin site
for model_class in model_classes:
    admin.site.register(model_class)