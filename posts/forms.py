from django import forms
from django.forms import ModelForm

from .models import Post, Comments


# Максим, здравствуйте. очень не привычно, прятать различные варианты в гит. Но, опыт, необычный и позновательный, спасибо.
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text", 'image']
        widgets = {
            "text": forms.Textarea()
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["text"]
        widgets = {
            "text": forms.Textarea()
        }
