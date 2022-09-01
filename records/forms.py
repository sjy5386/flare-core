from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = ['created_at', 'updated_at', 'provider_id', 'subdomain_name', 'domain']

    def __init__(self, *args, **kwargs):
        readonly_fields = kwargs.get('readonly_fields', [])
        if 'readonly_fields' in kwargs:
            del kwargs['readonly_fields']
        super(RecordForm, self).__init__(*args, **kwargs)
        for field in ['service', 'protocol', 'priority', 'weight', 'port']:
            self.fields[field].required = False
        for readonly_field in readonly_fields:
            self.fields[readonly_field].widget.attrs.update({
                'readonly': True,
            })


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea,
                           help_text='Name TTL Class Type Data e.g. example 3600 IN A 127.0.0.1')
