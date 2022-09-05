from django import forms

from .models import ShortUrl


class ShortUrlForm(forms.ModelForm):
    class Meta:
        model = ShortUrl
        fields = ['domain', 'name', 'long_url']


class ShortUrlLiteForm(ShortUrlForm):
    domain = None
    name = None
