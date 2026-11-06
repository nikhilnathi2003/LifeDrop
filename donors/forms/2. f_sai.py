"""Sai Srinivas Uppara — MessageForm, ReportForm."""
from django import forms

from ..models import Message
from ._base import bootstrap


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your message…"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)

    def clean_body(self):
        body = self.cleaned_data.get("body", "").strip()
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body


# ReportForm (for reporting a request/message) per the roles slide.
class ReportForm(forms.Form):
    REASONS = [
        ("spam", "Spam or scam"),
        ("fake", "Looks fake"),
        ("duplicate", "Duplicate request"),
        ("other", "Other"),
    ]
    reason = forms.ChoiceField(choices=REASONS)
    details = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
