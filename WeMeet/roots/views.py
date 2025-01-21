from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('Hello, World!')
  
def room(request):
    return HttpResponse('This is a room!')
# Create your views here.
