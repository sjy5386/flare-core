from django import forms

from .models import ShortUrl


class ShortUrlForm(forms.ModelForm):
    class Meta:
        model = ShortUrl
        fields = ['domain', 'name', 'long_url']


class ShortUrlLiteForm(forms.Form):
    long_url = forms.URLField(label='Long URL', max_length=2047)
