from django import forms

from .models import Comment, Post, Profile


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