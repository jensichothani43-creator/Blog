from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Create Post
    path('post/create/', views.create_post, name='create_post'),

    # Post detail
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # Edit
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),

    # Delete
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    # Like
    path('post/<int:pk>/like/', views.like_post, name='like_post'),

    # Register
    path('register/', views.register, name='register'),

    # Edit Profile (upload photo/bio) - must come before author_profile
    path(
    'profile/edit/',
        views.edit_profile,
        name='edit_profile',
    ),

    # Author Profile
    path(
        'profile/<str:username>/',
        views.author_profile,
        name='author_profile',
    ),
    path(
    "comment/<int:pk>/reply/",
    views.reply_comment,
    name="reply_comment",
),
path(
    "profile/<str:username>/posts/",
    views.profile_posts,
    name="profile_posts",
),

path(
    "profile/<str:username>/likes/",
    views.profile_likes,
    name="profile_likes",
),

path(
    "profile/<str:username>/comments/",
    views.profile_comments,
    name="profile_comments",
),
]