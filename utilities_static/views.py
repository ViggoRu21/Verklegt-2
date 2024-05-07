from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'landing.html')


def choose(request):
    # return HttpResponse("This is the login page.")
    return render(request, 'choose.html')

