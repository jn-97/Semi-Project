from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserForm, CustomUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def signup(req):
    if req.method == 'POST':
        user_form = CustomUserForm(req.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(req, user)
            return redirect('restaurants:index')
    else:
        user_form = CustomUserForm()
    cxt = {
        'user_form' : user_form
    }
    return render(req, 'accounts/signup.html', cxt)

@login_required
def delete(req, pk):
    user = get_user_model().objects.get(pk=pk)
    user.delete()
    logout(req, user)
    return redirect('accounts:any')

def log_in(req):
    if req.method == 'POST':
        login_form = AuthenticationForm(req, data=req.POST)
        if login_form.is_valid():
            login(req, login_form.get_user())
            return redirect(req.GET.get('next') or 'restaurants:index')
    else:
        login_form = AuthenticationForm()
    cxt = {
        'login_form' : login_form
    }
    return render(req, 'accounts/login.html', cxt)

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
