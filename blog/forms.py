from django import forms
from .models import Post, Comment # Importar Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date']
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Seu Comentário',
        }