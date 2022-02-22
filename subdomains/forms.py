from django import forms

from .models import Contact, Subdomain


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['created_at', 'updated_at', 'user']


class SubdomainForm(forms.ModelForm):
    class Meta:
        model = Subdomain
        exclude = ['created_at', 'updated_at', 'user', 'expiry', 'status']


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(min_value=0)
    record_type = forms.CharField()
    data = forms.CharField()
