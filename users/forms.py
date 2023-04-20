from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', ]


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', ]
