import datetime
from django.shortcuts import render, redirect
from .models import Restaurant, Comment
from .forms import RestaurantForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg

def index(request):
    restaurants = Restaurant.objects.order_by('-pk')
    context = {
        "restaurants": restaurants,
    }
    return render(request, "restaurants/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if restaurant_form.is_valid():
            form = restaurant_form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "작성되었습니다.")
            return redirect("restaurants:index")
    else:
        restaurant_form = RestaurantForm()
    context = {
        "restaurant_form": restaurant_form,
    }
    return render(request, "restaurants/create.html", context)

def detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    comments = restaurant.comment_set.all()
    form = CommentForm()
    default_hits = restaurant.hits
    restaurant.hits = default_hits + 1
    restaurant.save()
    context = {
        "restaurant": restaurant,
        "comments": comments,
        "form": form,
    }
    return render(request, "restaurants/detail.html", context)

@login_required
def update(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.user == restaurant.user:
        if request.method == 'POST':
            restaurant_form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
            if restaurant_form.is_valid():
                restaurant_form.save()
                messages.success(request, "수정되었습니다.")
                return redirect("restaurants:detail", pk)
        else:
            restaurant_form = RestaurantForm(instance=restaurant)
        
        context = {
            'restaurant_form': restaurant_form,
        }
        return render(request, "restaurants/update.html", context)
    else:
        messages.warning(request, "작성자만 수정 가능합니다.")
        return redirect("restaurants:detail", pk)

@login_required
def delete(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.user == restaurant.user:
        restaurant.delete()
        return redirect("restaurants:index")
    else:
        messages.warning(request, "작성자만 삭제 가능합니다.")
        return redirect("restaurants:detail", pk)


# 좋아요
@login_required
def like(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if restaurant.want_go.filter(pk=request.user.pk).exists():
        restaurant.want_go.remove(request.user)
    else:
        restaurant.want_go.add(request.user)

    return redirect("restaurants:detail", pk)

@login_required
def comment_create(request, pk):
    restaurant_data = Restaurant.objects.get(pk=pk)

    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant_data
            comment.user = request.user
            comment.save()

        return redirect('restaurants:detail', pk)
    
    else:
        return redirect('accounts:login')

@login_required
def comment_delete(request, pk, comment_pk):
    comment_data = Comment.objects.get(pk=comment_pk)

    if request.user == comment_data.user:
        comment_data.delete()
    else:
        messages.warning(request, "작성자만 삭제 가능합니다.")
    return redirect('restaurants:detail', pk)