"""Nikhil Goud Nathi — DonorProfile and DonorVerification."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .m_sujith import BloodType


class DonorProfile(models.Model):
    """A donor's account details, one-to-one with the Django user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor_profile")
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    last_donation = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        app_label = "donors"

    def __str__(self):
        return f"Donor {self.user.username}"

    @property
    def is_verified(self):
        return self.user.verifications.filter(status="approved").exists()


class DonorVerification(models.Model):
    """A donor-card document uploaded for the 'Verified donor' badge."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verifications")
    donor_card = models.FileField(upload_to="donor_cards/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Card of {self.user.username} ({self.status})"
