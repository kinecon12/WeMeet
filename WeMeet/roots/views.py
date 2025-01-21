from django.shortcuts import render
from django.http import HttpResponse
from .models import Room



def home(request):
  rooms = Room.objects.all()
  contest = {'rooms': rooms}
  return render(request,'roots/home.html', contest)
  
def room(request, pk):
  room = None
  for i in rooms:
    if i['id'] == int(pk):
      room = i
      contest = {'room': room}
    return render(request, 'roots/room.html', contest)
# Create your views here.
