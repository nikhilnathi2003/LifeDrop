"""Sai Srinivas Uppara — Message and UserVisit."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .m_sujith import BloodRequest


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
