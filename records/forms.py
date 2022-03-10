from django import forms


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(min_value=0, initial=3600)
    r_type = forms.CharField(initial='A')
    data = forms.CharField()


class ZoneImportForm(forms.Form):
    zone = forms.CharField(widget=forms.Textarea)
