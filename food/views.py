from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import is_user_authenticated
from django.contrib.auth.models import User
# from . forms import OrderForm


@is_user_authenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'food/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    clients = User.objects.all()
    clients = clients.filter(is_staff=False)
    context = {'clients': clients}
    return render(request, 'food/home.html', context)
