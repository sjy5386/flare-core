from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}


class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)
