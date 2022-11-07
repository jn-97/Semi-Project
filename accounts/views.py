from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserForm, CustomUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate
# Create your views here.

def signup(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        if user_form.is_valid():
            # email = user_form.cleaned_data.get('email').lower()
            # pass_word = user_form.cleaned_data.get('password1')
            user = user_form.save()
            login(request, user)
            return redirect('restaurants:index')
    else:
        user_form = CustomUserForm()
    context = {
        'user_form' : user_form
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.delete()
    logout(request, user)
    return redirect('accounts:any')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('restaurants:index')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password1']

        try:
            user = get_user_model().objects.get(username=username)
        except:
            messages.error(request, 'username does not exist!')
        

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:login')
        else:
            messages.error(request, 'username or password is incorrect!')

    return render(request, 'accounts/login.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('restaurants:index')

def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user' : user
    }
    return render(request, 'accounts/detail.html', context)

@login_required
def update(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == 'POST':
        update_user = CustomUpdateForm(request.POST, request.FILES, instance=user)
        if update_user.is_valid():
            update_user.save()
            return redirect('accounts:detail', pk)
    else:
        update_user = CustomUpdateForm(instance=user)
    context = {
        'update_user' : update_user
    }
    return render(request, 'accounts/update.html', context)

@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if user != request.user:
        if request.user.following.filter(pk=pk).exists():
            request.user.following.remove(user)
        else:
            request.user.following.add(user)
    return redirect('accounts:detail', pk)
