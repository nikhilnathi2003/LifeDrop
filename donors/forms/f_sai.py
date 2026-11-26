"""Sai Srinivas Uppara — MessageForm, ReportForm, GuestOfferForm."""
from django import forms

from ..models import Message, GuestOffer
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


class GuestOfferForm(forms.ModelForm):
    """Lets a guest (not signed in) offer to donate — only name + phone required."""
    class Meta:
        model = GuestOffer
        fields = ["name", "phone", "email", "blood_type", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3,
                        "placeholder": "Anything the family should know (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
        # GA requirement: a guest must leave at least a mobile OR an email so the
        # family can contact them, but they do NOT need to create an account.
        self.fields["phone"].required = False
        self.fields["email"].required = False
        self.fields["blood_type"].required = False
        self.fields["blood_type"].empty_label = "I'm not sure"
        self.fields["name"].widget.attrs["placeholder"] = "Your full name"
        self.fields["phone"].widget.attrs["placeholder"] = "Mobile number"
        self.fields["email"].widget.attrs["placeholder"] = "Email address"

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if phone:
            digits = [c for c in phone if c.isdigit()]
            if len(digits) < 7:
                raise forms.ValidationError("Please enter a valid mobile number.")
        return phone

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("phone") and not cleaned.get("email"):
            raise forms.ValidationError(
                "Please leave a mobile number or an email so the family can contact "
                "you about your donation.")
        return cleaned


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
