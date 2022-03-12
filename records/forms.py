from django import forms

from .types import Record


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(label='TTL', min_value=0, initial=3600)
    r_type = forms.ChoiceField(label='Type', choices=sorted(map(lambda e: (e, e), Record.get_available_types())),
                               initial='A')
    data = forms.CharField()


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea)
