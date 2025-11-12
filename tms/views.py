from django.shortcuts import render, redirect
from tms.forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        if request.user.role == 'staff':
            logout(request)
    return render(request, 'home.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        form.is_valid()
        form.save()
        return redirect('login')
    return render(request, "register.html", {"form":form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user = request.user
            if user.role == 'staff':
                return redirect('admindashboard')
           
            else:
                return redirect('homepage')
    return render(request, 'login.html')


    
def user_logout(request):
    logout(request)
    return redirect('homepage')