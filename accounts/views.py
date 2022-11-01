from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def signup(req):
    if req.method == 'POST':
        user_form = CustomUserForm(req.method)
        if user_form.is_valid():
            user = user_form.save()
            login(req, user)
            return render(req, 'accounts/any.html')
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
        login(req, login_form.get_user())
        return redirect(req.GET.get('next') or 'articles:index')
    else:
        login_form = AuthenticationForm()
    cxt = {
        'login_form' : login_form
    }
    return redirect('accounts:any')

def log_out(req):
    logout(req)
    return redirect('accounts:any')