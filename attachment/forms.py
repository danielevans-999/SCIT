from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'user_type')

    USER_TYPES = (

        ('admin', "Admin"),
        ('employer', "Employer"),
        ('supervisor', "Supervisor"),
        ('student', "Student"),
    )
    user_type = forms.ChoiceField(widget=forms.Select(attrs={
        'class': "form-control",
    }
    ), choices=USER_TYPES, label='Register As:')

    email = forms.Field(widget=forms.EmailInput(attrs={
        'class': "form-control",
        'placeholder': "Email"
    }), label='')

    username = forms.Field(widget=forms.TextInput(attrs={
        'class': "form-control",
        "placeholder": "username"
    }), label='')


    password1 = forms.Field(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        "placeholder": "Enter password",
    }), label='')

    password2 = forms.Field(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        "placeholder": "confirm password",

    }), label='')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
