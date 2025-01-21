from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


def home(request):
  rooms = Room.objects.all()
  contest = {'rooms': rooms}
  return render(request,'roots/home.html', contest)
  
def room(request, pk):
  rooms = Room.objects.get(id=pk)
  contest = {'room': room}
  return render(request, 'roots/room.html', contest)
# Create your views here.
def createRoom(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  contest = {'form': form}
  return render(request, 'roots/room_form.html', contest)