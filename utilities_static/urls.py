from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('choose', views.choose, name='choose')
]
