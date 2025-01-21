from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm


def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(description__icontains=q) | Q(name__icontains=q))
  topics = Topic.objects.all()
  room_count = rooms.count()
  contest = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
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

def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  contest = {'form': form}
  return render(request, 'roots/room_form.html', contest)

def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  contest = {'obj': room}
  return render(request, 'roots/delete.html', contest)