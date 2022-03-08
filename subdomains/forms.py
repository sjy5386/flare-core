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


class SubdomainContactForm(forms.Form):
    subdomain_name = forms.CharField()
    contacts = forms.MultipleChoiceField(choices=[
        ('registrant', 'Registrant'), ('admin', 'Admin'), ('tech', 'Tech'), ('billing', 'Billing')
    ], widget=forms.CheckboxSelectMultiple)
    your_name = forms.CharField()
    your_email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class SubdomainForm(forms.ModelForm):
    class Meta:
        model = Subdomain
        exclude = ['created_at', 'updated_at', 'user', 'expiry', 'status']


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(min_value=0)
    r_type = forms.CharField()
    data = forms.CharField()
