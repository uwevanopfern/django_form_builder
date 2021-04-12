from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import is_user_authenticated
from django.contrib.auth.models import User
# from . forms import OrderForm
from forms_builder.forms.models import Form


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


def forms(request):
    context =  {"forms": get_forms()}
    return render(request, 'food/forms.html',context) 

@login_required(login_url='login')
def home(request):
    clients = User.objects.all()
    clients = clients.filter(is_staff=False)
    context = {'clients': clients}
    return render(request, 'food/home.html', context)


@login_required(login_url='login')
def client_details(request, pk):
    client = get_client(pk=pk)
    context = {'client': client, "forms": get_forms()}
    return render(request, 'food/client_details.html', context)

@login_required(login_url='login')
def assign_forms(request):

    if request.method == 'POST':

        forms = request.POST.getlist('forms')
        client_id = request.POST.get('client_id')
        client = get_client(pk=client_id)
        context = {'client': client, "forms": get_forms()}

        if not forms:
            messages.info(request, 'Please select atleast one form')
            return render(request, 'food/client_details.html', context)
        else:
            if client is not None:
                messages.info(request, 'Form assigned to a user successfully')
                return redirect('home')
            else:
                messages.info(request, 'Error occured while assigning form to a client, Try again!!')
            
    return render(request, 'food/client_details.html', context)


def get_forms():
    return  Form.objects.all()

def get_client(pk):
    client = User.objects.get(pk=pk)
    return client
