from django.urls import path
from .views import user_search_view, register_view, login_view, landing_view, profile_view, edit_profile_view, delete_account_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('search/', user_search_view, name='user_search'),
    path('', landing_view, name='landing'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('delete_account/', delete_account_view, name='delete_account'),
    path('profile/<int:user_id>/delete/<int:post_id>/', profile_view, name='delete_post'),
]