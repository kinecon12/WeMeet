from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required   
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'User does not exit')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username OR password is incorrect')
  contest = {}
  return render(request, 'roots/login_register.html', contest)

def logoutUser(request):
  logout(request)
  return redirect('home')

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

@login_required(login_url= 'login')
def createRoom(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  contest = {'form': form}
  return render(request, 'roots/room_form.html', contest)

@login_required(login_url= 'login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  
  if request.user != room.host:
    return HttpResponse('You are not allowed')
  
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  contest = {'form': form}
  return render(request, 'roots/room_form.html', contest)

@login_required(login_url= 'login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  
  if request.user != room.host:
    return HttpResponse('You are not allowed')
  
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  contest = {'obj': room}
  return render(request, 'roots/delete.html', contest)