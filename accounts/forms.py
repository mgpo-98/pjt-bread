from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User

from django.contrib.auth import get_user_model
from django import forms
from .models import Profile




class CustomUserCreationForm(UserCreationForm):


    # username => 닉네임(아이디)
    username = forms.CharField(
        label ='닉네임(아이디)',
        widget=forms.TextInput(attrs={
            'placeholder' : '닉네임(아이디)'
        })
    )
    # first_name => 이름
    first_name = forms.CharField(
        label ='이름',
        widget=forms.TextInput(attrs={
            'placeholder' : '이름'
        })
    )
    # last_name => 성별

    
    
    
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','email','gender')



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# class CustomUserChangeForm(UserChangeForm):
#     class Meta():
#         model = get_user_model
#         fields = ('email', 'first_name', 'username')
class CustomUserChangeForm(UserChangeForm):
    password = None
        # username => 닉네임(아이디)
    username = forms.CharField(
        label ='닉네임(아이디)',
        widget=forms.TextInput(attrs={
            'placeholder' : '닉네임(아이디)'
        })
    )
    # first_name => 이름
    first_name = forms.CharField(
        label ='이름',
        widget=forms.TextInput(attrs={
            'placeholder' : '이름'
        })
    )
    # last_name => 성별
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','email','gender')
