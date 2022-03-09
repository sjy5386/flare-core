from django import forms

from contacts.models import Contact
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
    def __init__(self, user, *args, **kwargs):
        super(SubdomainForm, self).__init__(*args, **kwargs)
        contact_queryset = Contact.objects.filter(user=user)
        self.fields['registrant'] = forms.ModelChoiceField(queryset=contact_queryset)
        self.fields['admin'] = forms.ModelChoiceField(queryset=contact_queryset)
        self.fields['tech'] = forms.ModelChoiceField(queryset=contact_queryset)
        self.fields['billing'] = forms.ModelChoiceField(queryset=contact_queryset)

    class Meta:
        model = Subdomain
        fields = ['name', 'domain', 'is_private']
