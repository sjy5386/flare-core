from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = ['created_at', 'updated_at', 'provider_id', 'subdomain_name', 'domain']

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        for field in ['service', 'protocol', 'priority', 'weight', 'port']:
            self.fields[field].required = False


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea,
                           help_text='Name TTL Class Type Data e.g. example 3600 IN A 127.0.0.1')
