from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
import random

# Create your views here.
@require_safe
def index(request):
    reviews = Review.objects.order_by('-pk')
    request.GET.get('shop_name')
    context = {
        'reviews': reviews,
        'shop_name': request.GET.get('shop_name')
    }
    return render(request, 'reviews/index.html', context)

@login_required # 로그인한 경우에만 리뷰 작성 가능
def create(request, shop_id):
    shop_name = request.GET.get('shop_name')
    # print(request.GET.get('shop_name'))
    # print(shop_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            review.user = request.user 
            review.shop_id = shop_id
            review.shop_name = shop_name 
            review.save()
            messages.success(request, '리뷰 작성이 완료되었습니다.')
            return redirect('reviews:index')
    else: 
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
        'shop_name': request.GET.get('shop_name')
    }
    return render(request, 'reviews/form.html', context=context)

def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comment_form = CommentForm()
    # template에 객체 전달
    context = {
        'review': review,
        'comments': review.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            # POST : input 값 가져와서, 검증하고, DB에 저장
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                # 유효성 검사 통과하면 저장하고, 상세보기 페이지로
                review_form.save()
                messages.success(request, "리뷰가 수정되었습니다.")
                return redirect("reviews:detail", review.pk)
            # 유효성 검사 통과하지 않으면 => context 부터해서 오류메시지 담긴 review_form을 랜더링
        else:
            # GET : Form을 제공
            review_form = ReviewForm(instance=review)
        context = {
            "review_form": review_form,
            'shop_name': review.shop_name
        }
        return render(request, "reviews/form.html", context)
    else:
        # 작성자가 아닐 때
        # (1) 403 에러메시지를 던져버린다.
        # from django.http import HttpResponseForbidden
        # return HttpResponseForbidden()
        # (2) flash message 활용!
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("reviews:detail", review.pk)

@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("reviews:detail", review.pk)

def comment_delete(request, comment_pk, pk): # 마지막에 특정 리뷰에 대한 pk가 필요함
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("reviews:detail", pk)

@login_required
def like(request, pk):
    review = get_object_or_404(Review, pk=pk)
    # 만약 로그인한 유저(request.user)가 이 글을 좋아요 눌렀다면,
    if request.user in review.like_users.all():
        # 좋아요 삭제하고
        review.like_users.remove(request.user)
        is_liked = False
    else:  # 좋아요 누르지 않은 상태라면 좋아요에 추가하고
        review.like_users.add(request.user)
        is_liked = True
        # 상세 페이지로 redirect
        context = {"isLiked": is_liked, "likeCount": review.like_users.count()}
    return redirect("reviews:detail", review.pk)


# 리뷰 삭제
@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:index')
    context = {
        'review':review
    }
    return render(request, 'reviews/detail.html', context)