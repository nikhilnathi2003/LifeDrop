"""Venkata Charan Sai Doniparthi — ImageForm, SearchForm."""
from django import forms

from ..models import RequestImage, BloodType
from ._base import bootstrap


class ImageForm(forms.ModelForm):
    class Meta:
        model = RequestImage
        fields = ["image", "caption"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)


class SearchForm(forms.Form):
    """Keyword box plus the blood-type and city filters shown in the navbar."""
    keyword = forms.CharField(required=False, max_length=120)
    blood_type = forms.ModelChoiceField(queryset=BloodType.objects.all(), required=False,
                                        empty_label="All blood types")
    city = forms.CharField(required=False, max_length=60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
        self.fields["keyword"].widget.attrs["placeholder"] = "Search hospital, patient…"
        self.fields["city"].widget.attrs["placeholder"] = "City"
