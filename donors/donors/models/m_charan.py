"""Venkata Charan Sai Doniparthi — RequestImage and SearchQuery."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .m_sujith import BloodType, BloodRequest


class RequestImage(models.Model):
    """A photo attached to a request (e.g. the requisition slip)."""
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="requests/")
    caption = models.CharField(max_length=120, blank=True)

    class Meta:
        app_label = "donors"

    def __str__(self):
        return f"Image for {self.request}"


class SearchQuery(models.Model):
    """A search a user ran, kept for the 'recent searches' history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches",
                             null=True, blank=True)
    keyword = models.CharField(max_length=120, blank=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "donors"
        ordering = ["-date"]
        verbose_name_plural = "search queries"

    def __str__(self):
        return self.keyword or "(empty search)"
