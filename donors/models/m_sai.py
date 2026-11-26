"""Sai Srinivas Uppara — Message, UserVisit and GuestOffer."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .m_sujith import BloodRequest, BloodType


class Message(models.Model):
    """A message between a requester and a potential donor about a request."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name="messages",
                                null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


class UserVisit(models.Model):
    """Counts how many times a user visited the site on a given day."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    date = models.DateField(default=timezone.now)
    visit_count = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = "donors"
        ordering = ["-date"]
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user.username} on {self.date}: {self.visit_count}"


class GuestOffer(models.Model):
    """A donation offer left by a guest who is NOT signed in.

    This is the GA-requested feature: anyone can offer to donate without an
    account, just by leaving their name and a phone number so the family can
    reach them. The requester sees these offers on their request and inbox.
    """
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE,
                                related_name="guest_offers")
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Guest offer by {self.name} for {self.request}"
