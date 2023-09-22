from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return HttpResponse("<h1> Module auth </h1>")
def signup(request):
    if request.method == "GET":
        return render(request,"signup.html")
    else:
        if request.POST['password1'] != request.POST['password2']:
            return HttpResponse(" passwords do not match ")
        # register user
        try:
            user_nuevo = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
            user_nuevo.save()
            login(request,user_nuevo)
            return render(request,'welcome.html')
        except:
            return HttpResponse(" User exists ")

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html')
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if not user:
            return HttpResponse(" Password incorrect")
        else:
            login(request,user)
            return redirect('/')

def signout(request):
    logout(request)
    return redirect('/')
