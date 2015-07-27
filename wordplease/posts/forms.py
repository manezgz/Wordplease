
from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    """
    Formulario para el modelo Post
    """

    class Meta:
        model = Post
        exclude = ['owner']