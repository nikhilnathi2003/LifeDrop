"""Nikhil Goud Nathi — RegisterForm, DonorProfileForm, DonorVerificationForm."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ..models import DonorProfile, DonorVerification
from ._base import bootstrap


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ["blood_type", "city", "phone", "last_donation", "available"]
        widgets = {"last_donation": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)


class DonorVerificationForm(forms.ModelForm):
    class Meta:
        model = DonorVerification
        fields = ["donor_card"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap(self.fields)
