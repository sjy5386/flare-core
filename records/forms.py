from django import forms

from .types import Record


class BaseRecordForm(forms.Form):
    name = forms.CharField(max_length=255)
    ttl = forms.IntegerField(label='TTL', min_value=0, initial=3600)
    r_type = forms.ChoiceField(label='Type',
                               choices=sorted(
                                   map(lambda e: (e[0], f'{e[0]} - {e[1]}'), Record.get_available_types().items())),
                               initial='A')
    data = forms.CharField()


class RecordForm(BaseRecordForm):
    data = None

    service = forms.CharField(required=False, help_text='Required for SRV record.')
    protocol = forms.CharField(required=False, help_text='Required for SRV record.')

    priority = forms.IntegerField(min_value=0, max_value=65535, required=False,
                                  help_text='Required for MX and SRV records.')
    weight = forms.IntegerField(min_value=0, max_value=65535, required=False, help_text='Required for SRV record.')
    port = forms.IntegerField(min_value=0, max_value=65535, required=False, help_text='Required for SRV record.')

    target = forms.CharField()


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea)
