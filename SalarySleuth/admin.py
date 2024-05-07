from django.contrib import admin
from SalarySleuth.models import *

model_classes = [cls for name, cls in vars().items() if isinstance(cls, type) and issubclass(cls, models.Model)]

for model_class in model_classes:
    admin.site.register(model_class)
