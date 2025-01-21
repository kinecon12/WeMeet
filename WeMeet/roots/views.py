from django.shortcuts import render
from django.http import HttpResponse

rooms = [
  {'id': 1, 'name': 'Room 1'},
  {'id': 2, 'name': 'Room 2'},
  {'id': 3, 'name': 'Room 3'},
]

def home(request):
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
