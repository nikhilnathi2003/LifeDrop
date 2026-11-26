"""Sujith Chitram — BloodType and BloodRequest."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class BloodType(models.Model):
    """A blood group, e.g. O+, O-, A+, B-."""
    name = models.CharField(max_length=4, unique=True)
    slug = models.SlugField(max_length=10, unique=True, blank=True)

    class Meta:
        app_label = "donors"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("+", "-pos").replace("-", "-neg"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BloodRequest(models.Model):
    """A request for blood of a certain type at a hospital."""
    URGENCY_CHOICES = [
        ("normal", "Normal"),
        ("urgent", "Urgent"),
        ("critical", "Critical"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("matched", "Matched"),
        ("fulfilled", "Fulfilled"),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    blood_type = models.ForeignKey(BloodType, on_delete=models.PROTECT, related_name="requests")
    patient = models.CharField(max_length=120, help_text="Patient name or a short title")
    hospital = models.CharField(max_length=160)
    city = models.CharField(max_length=60)
    units = models.PositiveSmallIntegerField(default=1)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default="urgent")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.blood_type} for {self.patient}"
