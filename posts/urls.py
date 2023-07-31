from django.urls import path
from .views import feed_view, new_post_view, logout_view, like_post_view, likes_view, comment_post_view, comments_view

urlpatterns = [
    path('feed/', feed_view, name='feed'),
    path('new/', new_post_view, name='new_post'),
    path('logout/', logout_view, name='logout'),
    path('like_post/<int:post_id>/', like_post_view, name='like_post'),
    path('comment_post/<int:post_id>/', comment_post_view, name='comment_post'),
    path('post/<int:post_id>/comments/', comments_view, name='comments'),
    path('post/<int:post_id>/likes/', likes_view, name='likes'),
]