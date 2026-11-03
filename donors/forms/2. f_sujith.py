"""Sujith Chitram — RequestForm, EditRequestForm."""
from django import forms

from ..models import BloodRequest
from ._base import bootstrap


class RequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ["patient", "blood_type", "hospital", "city", "units", "urgency", "status", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
        self.fields["notes"].widget.attrs["rows"] = 3

    def clean_patient(self):
        patient = self.cleaned_data.get("patient", "").strip()
        if len(patient) < 2:
            raise forms.ValidationError("Please enter a patient name or title.")
        return patient

    def clean_units(self):
        units = self.cleaned_data.get("units")
        if units is not None and units < 1:
            raise forms.ValidationError("At least one unit is required.")
        return units


# EditRequestForm reuses the same fields; kept as its own name per the roles slide.
class EditRequestForm(RequestForm):
    pass
