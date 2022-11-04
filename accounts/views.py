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
    cxt = {
        'user_form' : user_form
    }
    return render(request, 'accounts/signup.html', cxt)

@login_required
def delete(req, pk):
    user = get_user_model().objects.get(pk=pk)
    user.delete()
    logout(req, user)
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
def log_out(req):
    logout(req)
    return redirect('restaurants:index')

def detail(req, pk):
    user = get_user_model().objects.get(pk=pk)
    cxt = {
        'user' : user
    }
    return render(req, 'accounts/detail.html', cxt)

@login_required
def update(req, pk):
    user = get_user_model().objects.get(pk=pk)
    if req.method == 'POST':
        update_user = CustomUpdateForm(req.POST, req.FILES, instance=user)
        if update_user.is_valid():
            update_user.save()
            return redirect('accounts:detail', pk)
    else:
        update_user = CustomUpdateForm(instance=user)
    cxt = {
        'update_user' : update_user
    }
    return render(req, 'accounts/update.html', cxt)

@login_required
def follow(req, pk):
    user = get_user_model().objects.get(pk=pk)
    if user != req.user:
        if req.user.following.filter(pk=pk).exists():
            req.user.following.remove(user)
        else:
            req.user.following.add(user)
    return redirect('accounts:detail', pk)
