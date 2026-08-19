from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        unique=True,
    )

    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_detail",
            kwargs={"slug": self.slug},
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()

    # Reply / Parent comment
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.post.title}"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.user.username


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="unique_post_like",
            )
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"