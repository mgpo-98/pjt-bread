from django import forms
from .models import Review, Comment
from django.forms.widgets import DateInput


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['image', 'content', 'visited_at']
        widgets = {
            'visited_at': DateInput(attrs={'type': 'date'}),
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]