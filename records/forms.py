from django import forms

from .types import Record


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(label='TTL', min_value=0, initial=3600)
    r_type = forms.ChoiceField(label='Type',
                               choices=sorted(
                                   map(lambda e: (e[0], f'{e[0]} - {e[1]}'), Record.get_available_types().items())),
                               initial='A')
    data = forms.CharField()


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea)
