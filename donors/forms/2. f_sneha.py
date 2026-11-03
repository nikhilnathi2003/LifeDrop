"""Sneha Gunturu — ContactForm, ReviewForm."""
from django import forms

from ..models import ContactMessage, Review
from ._base import bootstrap


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)


# TODO (Sneha): wire ReviewForm into a leave_review view (remaining ~40%).
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
