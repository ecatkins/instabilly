from django.forms import ModelForm
from spotify.models import User
from django import forms



class UserForm(ModelForm):
    class Meta:
            model = User
            fields = ['username', 'password']
            widgets = {
                'username': forms.TextInput(attrs={'required':'true'}),
                'password': forms.PasswordInput(attrs={'required':'true'})

            }

class RegistrationForm(ModelForm):
    class Meta:
            model = User
            fields = ['username', 'password', 'first_name', 'last_name', 'email']
            widgets = {
                'username': forms.TextInput(attrs={'required':'true'}),
                'password': forms.PasswordInput(attrs={'required':'true'}),
                'first_name': forms.TextInput(attrs={'required':'true'}),
                'last_name': forms.TextInput(attrs={'required':'true'}),
                'email': forms.EmailInput(attrs={'required':'true'})

            }