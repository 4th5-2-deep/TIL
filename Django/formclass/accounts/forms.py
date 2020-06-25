from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() #=> auth.User
        fields = ('username', 'email',
                'first_name', 'last_name',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'image', )
