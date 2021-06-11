
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Userprofile
# Create your views here.

def index(request):
    return render(request, '../templates/core/index.html')

def plans(request):
    return render(request, '../templates/core/plans.html')

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        messages.info(request, 'Изменения успешно сохранены')
    return render(request, '../templates/accounts/profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.first_name = 'Temporary'
            user.last_name = 'Name'
            user.save()
            uprofile = Userprofile.objects.create(user=user)
            login(request, user)
            return redirect('projects')
    else:
        form = UserCreationForm()
    return render(request, '../templates/core/signup.html', {'form': form})

def templates(request):
    return render(request, '../templates/core/templates.html')