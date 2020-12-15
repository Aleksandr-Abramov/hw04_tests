from django import forms
from django.forms import ModelForm

from .models import Post


# Максим, здравствуйте. очень не привычно, прятать различные варианты в гит. Но, опыт, необычный и позновательный, спасибо.
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text"]
        widgets = {
            "text": forms.Textarea()
        }
