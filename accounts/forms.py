# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomerSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=120, required=False)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "full_name", "phone", "address")

class FancyAuthenticationForm(AuthenticationForm):
    remember = forms.BooleanField(required=False, initial=False, help_text="Keep me signed in")
