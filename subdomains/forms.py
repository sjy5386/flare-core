from django import forms

from domains.models import Domain
from .models import Subdomain


class SubdomainSearchForm(forms.Form):
    q = forms.CharField(label='Name', max_length=63)
    domain = forms.ModelMultipleChoiceField(queryset=Domain.objects.filter(is_active=True),
                                            widget=forms.CheckboxSelectMultiple)
    hide_unavailable = forms.BooleanField(required=False)


class SubdomainWhoisForm(forms.Form):
    q = forms.CharField(label='Subdomain Name')


class SubdomainForm(forms.ModelForm):
    class Meta:
        model = Subdomain
        exclude = ['created_at', 'updated_at', 'user', 'expiry', 'status']


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(min_value=0)
    record_type = forms.CharField()
    data = forms.CharField()
