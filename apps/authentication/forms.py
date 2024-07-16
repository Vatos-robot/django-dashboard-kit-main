from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        ))
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        ))
    team = forms.ChoiceField(
        choices=CustomUser.TEAM_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'team', 'password1', 'password2')
