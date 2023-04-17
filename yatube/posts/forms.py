from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма создания Post."""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Форма создания Comment."""

    class Meta:
        model = Comment
        fields = ('text',)
