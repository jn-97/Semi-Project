from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "작성되었습니다.")
            return redirect("reviews:index", form.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)

@login_required
def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment = review.comment_set.all()
    form = CommentForm()

    context = {
        "review": review,
        "comment": comment,
        "form": form,
    }
    return render(request, "reviews/detail.html", context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "수정되었습니다.")
                return redirect("reviews:detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
        
        context = {
            'review_form': review_form,
        }
        return render(request, "reviews/update.html", context)
    else:
        messages.warning(request, "작성자만 수정 가능합니다.")
        return redirect("reviews:detail", pk)

@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        review.delete()
        return redirect("reviews:index")
    else:
        messages.warning(request, "작성자만 삭제 가능합니다.")
        return redirect("reviews:detail", pk)


# 좋아요
@login_required
def like(request, pk):
    review = Review.objects.get(pk=pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)

    return redirect("reviews:detail", pk)

@login_required
def comment_create(request, pk):
    review_data = Review.objects.get(pk=pk)

    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review_data
            comment.user = request.user
            comment.save()

        return redirect('reviews:detail', review_data.pk)
    
    else:
        return redirect('accounts:login')

@login_required
def comment_delete(request, pk, comment_pk):
    review_data = Review.objects.get(pk=pk)
    comment_data = review_data.comment_set.get(pk=comment_pk)

    if request.user == comment_data.user:
        comment_data.delete()
    else:
        messages.warning(request, "작성자만 삭제 가능합니다.")
    return redirect('reviews:detail', review_data.pk)
