from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, UserSearchForm, UserProfileForm
from .models import Following, UserProfile
from posts.models import Post
from notifications.models import Notification

# Create your views here.

def landing_view(request):
    return render(request, 'accounts/landing.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_search_view(request):
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            users = User.objects.filter(username__icontains=username)[:10]
            return render(request, 'posts/user_search_results.html', {'users': users, 'form': form})
    else:
        form = UserSearchForm()
    return render(request, 'accounts/user_search.html', {'form': form})

from django.http import JsonResponse

@login_required
def profile_view(request, user_id, post_id=None):
    user = User.objects.get(id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    following = Following.objects.filter(follower=request.user, followed=user).exists()

    # Delete post
    if request.method == "DELETE" and post_id:
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            post.delete()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'unauthorized'}, status=403)
        
    if request.method == "POST":
        if following:
            Following.objects.filter(follower=request.user, followed=user).delete()
        else:
            Notification.objects.create(user=profile.user, type=Notification.FOLLOW, extra_id=request.user.id, extra_info=request.user)
            Following.objects.create(follower=request.user, followed=user)
        return redirect('profile', user_id=user.id)
    return render(request, 'accounts/profile.html', {'profile_user': user, 'profile': profile, 'posts': posts, 'following': following})

@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('landing')
    else:
        return render(request, 'accounts/delete_account_confirm.html')