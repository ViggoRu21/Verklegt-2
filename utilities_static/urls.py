from django.urls import path
from . import views


app_name = 'utilities_static'


urlpatterns = [
    path('', views.home, name='landing'),
    path('choose', views.choose, name='choose')
]
