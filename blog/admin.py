from django.contrib import admin

from .models import Category, Comment, Like, Post



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "category",
        "created_at",
    ]

    search_fields = [
        "title",
        "content",
        "author__username",
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "post",
        "created_at",
    ]

    search_fields = [
        "content",
        "author__username",
    ]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "post",
        "created_at",
    ]