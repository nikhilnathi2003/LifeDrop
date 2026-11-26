"""Sneha Gunturu — ContactMessage and Review."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ContactMessage(models.Model):
    """A message sent through the Contact Us page."""
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.name})"


class Review(models.Model):
    """Feedback one user leaves for another after a donation."""
    RATING_CHOICES = [(i, f"{i} star" + ("s" if i != 1 else "")) for i in range(1, 6)]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_written")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}* for {self.user.username} by {self.reviewer.username}"
