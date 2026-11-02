"""Shared view helpers (user history via sessions + cookies)."""
from django.utils import timezone

from ..models import UserVisit

RECENT_LIMIT = 8


def track_visit(request):
    """Count a visit for today (DB) for a logged-in user."""
    if request.user.is_authenticated:
        visit, created = UserVisit.objects.get_or_create(
            user=request.user, date=timezone.now().date())
        if not created:
            visit.visit_count += 1
            visit.save(update_fields=["visit_count"])


def remember_recent(request, key, value, limit=RECENT_LIMIT):
    """Push a value to the front of a de-duplicated session list."""
    items = request.session.get(key, [])
    if value in items:
        items.remove(value)
    items.insert(0, value)
    request.session[key] = items[:limit]
    request.session.modified = True
