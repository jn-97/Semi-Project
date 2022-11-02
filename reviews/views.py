import datetime
from email.policy import default
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
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "작성되었습니다.")
            return redirect("reviews:index")
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
    # 단순 조회수
    default_hits = review.hits
    review.hits = default_hits + 1
    review.save()
    # session_cookie = request.session.get
    # cookie_name = F'reviews_hits:{session_cookie}'
    context = {
        "review": review,
        "comments": comment,
        "commentform": form,
    }

    return render(request, "reviews/detail.html", context)

    # # [1] 로그인 확인
    # if request.session.get('authUser') is None:
    #     cookie_name = 'hit'
    # else:
    #     cookie_name = f'hit:{request.session["authUser"]["id"]}'

    # # [2] 그 날 당일 밤 12시에 쿠키 삭제
    # tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    # expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    # # [3] hit를 check하는 쿠키가 있는 경우
    # if request.COOKIES.get(cookie_name) is not None:
    #     cookies = request.COOKIES.get(cookie_name)
    #     cookies_list = cookies.split('|')
    #     if str(pk) not in cookies_list:
    #         response.set_cookie(cookie_name, cookies + f'|{pk}', expires=expires)
    #         review.hits += 1
    #         review.save()
    #         return response

    # # [4] hit를 check하는 쿠키가 없는 경우
    # else:
    #     response.set_cookie(cookie_name, pk, expires=expires)
    #     review.hits += 1
    #     review.save()
    #     return response
        
    # return render(request, 'reviews/index.html', context)

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
