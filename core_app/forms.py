from django import forms
from django.forms import ModelForm, Textarea

from .models import Category, Comment, Post

choices = Category.objects.all().values_list("name", "name")

choice_list = []

for item in choices:
    choice_list.append(item)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "author", "category", "body"]

    widgets = {"category": forms.Select(choices=choice_list, attrs={"class": "form-control"})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]
        widgets = {
            "body": Textarea(attrs={"placeholder": "Comment here...", "rows": 8, "cols": 20})
        }

