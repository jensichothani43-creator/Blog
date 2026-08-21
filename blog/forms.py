from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, Profile


MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]


def validate_image(image):
    if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Image file too large. Maximum size is {MAX_IMAGE_SIZE_MB}MB."
        )

    content_type = getattr(image, "content_type", None)
    if content_type and content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            "Unsupported file type. Please upload a JPEG, PNG, WEBP, or GIF image."
        )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "category",
            "content",
            "image",

        ]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            validate_image(image)
        return image


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment...",
                }
            )
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["image", "bio"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            validate_image(image)
        return image