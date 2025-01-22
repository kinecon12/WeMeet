from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required   
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

def loginPage(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    username = request.POST.get('username').lower()
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
  contest = {'page': page }
  return render(request, 'roots/login_register.html', contest)

def logoutUser(request):
  logout(request)
  return redirect('home')

def registerPage(request):
  form = UserCreationForm()
  
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error has occured during registration')
  return render(request, 'roots/login_register.html', {'form': form})

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(description__icontains=q) | Q(name__icontains=q))
  topics = Topic.objects.all()
  room_count = rooms.count()
  room_messages = Message.objects.all()
  
  
  contest = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
  return render(request,'roots/home.html', contest)
  
def room(request, pk):
  rooms = Room.objects.get(id=pk)
  room_messages = rooms.message_set.all()
  participants = rooms.participants.all()
  if request.method == 'POST':
    message = Message.objects.create(
      user=request.user, 
      room=rooms, 
      body=request.POST.get('body')
      )
    rooms.participants.add(request.user)
    return redirect('room', pk=pk)
  contest = {'room': room, 'room_messages': room_messages, 'participants': participants}
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

@login_required(login_url= 'login')
def deletemessage(request, pk):
  message = Message.objects.get(id=pk)
  
  if request.user != message.user:
    return HttpResponse('You are not allowed')
  
  if request.method == 'POST':
    messages.delete()
    return redirect('home')
  contest = {'obj': message}
  return render(request, 'roots/delete.html', contest)