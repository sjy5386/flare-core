from django import forms


class RecordForm(forms.Form):
    name = forms.CharField()
    ttl = forms.IntegerField(min_value=0)
    r_type = forms.CharField()
    data = forms.CharField()
