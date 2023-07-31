
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewPostForm, CommentForm
from .models import Post, Like, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from accounts.forms import UserSearchForm
from django.contrib.auth.models import User
from django.db.models import Count
from notifications.models import Notification

# Create your views here.

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('landing')

@login_required
def feed_view(request):
    form = UserSearchForm()
    following = request.user.following.values_list('followed', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')

    # Get the 10 users with the most followers
    popular_users = User.objects.annotate(num_followers=Count('followers')).order_by('-num_followers')[:10]

    unread_notifications_count = Notification.objects.filter(user=request.user, read=False).count()

    return render(request, 'posts/feed.html', {'posts': posts, 'form': form, 'popular_users': popular_users, 'unread_notifications_count': unread_notifications_count})

@login_required
def new_post_view(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = NewPostForm()
    return render(request, 'posts/new_post.html', {'form': form})


@login_required
def like_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # The user already liked this post, so their click in this case is to unlike it
        like.delete()
    elif request.user != post.user:  # Don't create a notification if the user likes their own post
        Notification.objects.create(user=post.user, type=Notification.LIKE, extra_info=f'{request.user.username} liked your post')
    return redirect('feed')

@login_required
def comment_post_view(request, post_id):
    if request.method == "POST":
        comment_text = request.POST.get('comment')
        post = Post.objects.get(id=post_id)
        Comment.objects.create(user=request.user, post=post, text=comment_text)
    return redirect('feed')

@login_required
def likes_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = post.like_set.all()
    return render(request, 'posts/likes.html', {'post': post, 'likes': likes})

@login_required
def comments_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            if request.user != comment.post.user:  # Don't create a notification if the user comments on their own post
                Notification.objects.create(user=comment.post.user, type=Notification.COMMENT, extra_info=f'{request.user.username} commented on your post')

            return redirect('comments', post_id=post.id)
    else:
        form = CommentForm()
    comments = post.comment_set.all().order_by('-timestamp')
    return render(request, 'posts/comments.html', {'post': post, 'comments': comments, 'form': form})