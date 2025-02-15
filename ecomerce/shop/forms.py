from django import forms
from django.forms import PasswordInput
from django.contrib.auth.models import User

class Registrationform(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    confirm_password=forms.CharField(widget=PasswordInput)
    class Meta:
        model=User
        fields = ['username', 'password','confirm_password', 'email', 'first_name', 'last_name']