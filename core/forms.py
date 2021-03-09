from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from model_utils import Choices
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserAdditionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'status']


class UserAdditionForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'status', 'image']
