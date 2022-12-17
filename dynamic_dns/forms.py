from django import forms

from .models import AuthenticationToken


class AuthenticationTokenForm(forms.ModelForm):
    class Meta:
        model = AuthenticationToken
        fields = ('name', 'record',)
