from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import is_user_authenticated
from forms_builder.forms.models import Form
from .forms import ClientForm


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

def form_sent(request):
    return render(request, 'food/form_sent.html')

@login_required(login_url='login')
def fill_form(request, slug):
    form = ClientForm()
    if request.method == 'POST':
        pass
		# form = CreateUserForm(request.POST)
		# if form.is_valid():
		# 	user = form.save()
		# 	username = form.cleaned_data.get('username')

		# 	group = Group.objects.get(name='customer')
		# 	user.groups.add(group)

		# 	messages.success(request, 'Account was created for ' + username)

		# 	return redirect('login')
    context = {'form':form}
    return render(request, 'food/fill_form.html', context)

@login_required(login_url='login')
def home(request):
    clients = User.objects.all()
    clients = clients.filter(is_admin=False)
    user = User.objects.get(username=request.user)
    auth_forms = user.forms.all()
    context = {'clients': clients, 'auth_forms': auth_forms}
    return render(request, 'food/home.html', context)


@login_required(login_url='login')
def client_details(request, pk):
    client = get_client(pk=pk)
    client_forms = client.forms.all()
    forms = get_forms()
    context = {'client': client, 'client_forms': client_forms}
    return render(request, 'food/client_details.html', context)

def get_forms():
    return Form.objects.all()

def get_client(pk):
    client = User.objects.get(pk=pk)
    return client
