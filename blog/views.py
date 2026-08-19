from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render


from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Like, Post, Profile



# ============================================================
# HOME
# ============================================================

def home(request):
    """
    Display published blog posts with:
    - Search
    - Pagination
    - Categories
    """

    query = request.GET.get("q", "").strip()

    posts = (
    Post.objects
    .filter(status="approved")
    .select_related("author", "category")
)

    # Search
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
        )

    # Pagination
    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    # Categories
    categories = Category.objects.all()

    return render(
        request,
        "blog/home.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "query": query,
        },
    )


# ============================================================
# POST DETAIL
# ============================================================

def post_detail(request, slug):
    """
    Display a single published post with:
    - Comments
    - Like status
    """

    post = get_object_or_404(
        Post.objects.select_related(
            "author",
            "category",
        ),
        slug=slug,
        status="approved",
    )

    # Comments
    comments = (
    post.comments
    .select_related("author")
    .order_by("-created_at")
)
    # Like status
    liked = False

    if request.user.is_authenticated:
        liked = Like.objects.filter(
            post=post,
            user=request.user,
        ).exists()

    # Comment submission
    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post
            comment.author = request.user

            comment.save()

            messages.success(
                request,
                "Comment added successfully.",
            )

            return redirect(
                "post_detail",
                slug=post.slug,
            )

    else:
        form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": form,
            "liked": liked,
        },
    )


# ============================================================
# CREATE POST
# ============================================================
@login_required
def create_post(request):
    """
    Create a new blog post.
    New posts require admin approval.
    """

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            post = form.save(commit=False)

            # Current logged-in user becomes author
            post.author = request.user

            # New posts wait for admin approval
            post.status = "pending"

            post.save()

            messages.success(
                request,
                "Post submitted successfully. Waiting for admin approval.",
            )

            return redirect(
                "author_profile",
                username=request.user.username,
            )

    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "title": "Create Post",
        },
    )

# ============================================================
# PROFILE POSTS
# ============================================================

def profile_posts(request, username):

    author = get_object_or_404(
        User,
        username=username,
    )

    posts = (
        author.posts
        .filter(status="approved")
        .order_by("-created_at")
    )

    return render(
        request,
        "blog/profile_posts.html",
        {
            "author": author,
            "posts": posts,
        },
    )


# ============================================================
# PROFILE LIKES
# ============================================================

def profile_likes(request, username):

    author = get_object_or_404(
        User,
        username=username,
    )

    likes = (
        Like.objects
        .filter(user=author)
        .select_related("post", "post__author", "post__category")
        .order_by("-id")
    )

    return render(
        request,
        "blog/profile_likes.html",
        {
            "author": author,
            "likes": likes,
        },
    )


# ============================================================
# PROFILE COMMENTS
# ============================================================

def profile_comments(request, username):

    author = get_object_or_404(
        User,
        username=username,
    )

    comments = (
        Comment.objects
        .filter(author=author)
        .select_related("post", "post__author")
        .order_by("-created_at")
    )

    return render(
        request,
        "blog/profile_comments.html",
        {
            "author": author,
            "comments": comments,
        },
    )
# ============================================================
# UPDATE POST
# ============================================================

@login_required
def update_post(request, pk):
    """
    Update an existing post.
    Only the post owner can edit it.
    """

    post = get_object_or_404(
        Post,
        pk=pk,
    )

    # Author permission
    if post.author != request.user:

        messages.error(
            request,
            "You cannot edit this post.",
        )

        return redirect("home")

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Post updated successfully.",
            )

            return redirect(
                "post_detail",
                slug=post.slug,
            )

    else:
        form = PostForm(
            instance=post,
        )

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "title": "Update Post",
        },
    )


# ============================================================
# DELETE POST
# ============================================================

@login_required
def delete_post(request, pk):
    """
    Delete a post.
    Only the post owner can delete it.
    """

    post = get_object_or_404(
        Post,
        pk=pk,
    )

    # Author permission
    if post.author != request.user:

        messages.error(
            request,
            "You cannot delete this post.",
        )

        return redirect("home")

    if request.method == "POST":

        post.delete()

        messages.success(
            request,
            "Post deleted successfully.",
        )

        return redirect("home")

    return render(
        request,
        "blog/post_confirm_delete.html",
        {
            "post": post,
        },
    )


# ============================================================
# REPLY TO COMMENT
# ============================================================

@login_required
def reply_comment(request, pk):
    """
    Reply to an existing comment.
    """

    parent_comment = get_object_or_404(
        Comment,
        pk=pk,
    )

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            reply = form.save(commit=False)

            reply.post = parent_comment.post
            reply.author = request.user
            
           
            reply.save()

            messages.success(
                request,
                "Reply added successfully.",
            )

    return redirect(
        "post_detail",
        slug=parent_comment.post.slug,
    )

# ============================================================
# LIKE / UNLIKE POST
# ============================================================

@login_required
def like_post(request, pk):
    """
    Like or unlike a published post.
    """

    post = get_object_or_404(
        Post,
        pk=pk,
        status="approved",
    )

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user,
    )

    # Toggle like
    if not created:
        like.delete()

    return JsonResponse({
        "liked": created,
        "count": post.likes.count(),
    })

# ============================================================
# REGISTER
# ============================================================

def register(request):
    """
    Register a new user and automatically log them in.
    """

    # Already logged-in users don't need registration
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = UserCreationForm(
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            # Automatically login after registration
            login(
                request,
                user,
            )

            messages.success(
                request,
                "Account created successfully.",
            )

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )
# ============================================================
# EDIT PROFILE
# ============================================================

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect(
                "author_profile",
                username=request.user.username,
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "blog/edit_profile.html",
        {
            "form": form,
        },
    )
# ============================================================
# AUTHOR PROFILE
# ============================================================

def author_profile(request, username):

    author = get_object_or_404(
        User,
        username=username,
    )

    profile = getattr(
        author,
        "profile",
        None,
    )

    posts = (
        author.posts
        .filter(status="approved")
        .prefetch_related("likes", "comments")
        .order_by("-created_at")
    )

    total_likes = sum(
        post.likes.count()
        for post in posts
    )

    total_comments = sum(
        post.comments.count()
        for post in posts
    )

    return render(
        request,
        "blog/author_profile.html",
        {
            "author": author,
            "profile": profile,
            "posts": posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
        },
    )
