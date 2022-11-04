from django import forms
from .models import Review, Comment
from django.forms.widgets import DateInput, Textarea, TextInput, FileInput


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['image', 'content', 'visited_at']
        widgets = {
            'visited_at': DateInput(attrs={'type': 'date'}),
            'content': Textarea(attrs={'rows':4})
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': Textarea(attrs={'rows':4})

        }