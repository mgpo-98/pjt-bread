from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import User 
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.http import JsonResponse


# 인덱스
def index(request):
    users = get_user_model().objects.all()
    context = {
        'users':users,
    }
    return render(request, 'accounts/index.html', context)

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:   
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm (request.POST, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or '/')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('/')

# 회원 목록 조회 페이지
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user 
            profile.save()


            # 만약 이미지가 하나 더 있으면? 첫번째거를 지우고 추가
            if user.profile_set.all().count() > 1:
                user.profile_set.all()[0].delete()
                
            return redirect('accounts:index')
    else:
        profile_form = ProfileForm()
    
    if user.profile_set.all().count() == 0:
        profile_image = None
    else:
        profile_image = user.profile_set.all()[0]
    context = {
        'user' : user, 
        'profile_form' : profile_form,
        'profile_image' : profile_image,
    }
    return render(request, 'accounts/detail.html', context)

# 회원정보 업데이트
@login_required
def update(request, pk): 
    user = User.objects.get(pk=pk)
    if request.method =='POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context ={
        'form' : form,
    }
    return render(request, 'accounts/update.html', context )

#회원 탈퇴
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)

    return redirect('accounts:index')


# 팔로우


def follow(request, pk):
    if request.user.is_authenticated:
        User = get_user_model()
        me = request.user
        you = User.objects.get(pk=pk)
        if me != you:
            if you.followers.filter(pk=me.pk).exists():
                you.followers.remove(me)
                is_followed =False
            else :
                you.followers.add(me)
                is_followed = True
            context ={
                'is_followed' : is_followed,
                'followers_count' :  you.followers.count(),
                'followings_count' : you.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:detail', you.username)
    return redirect('accounts:login')

