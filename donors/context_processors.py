"""Values made available to every template (navbar search, blood types, unread count)."""
from .forms import SearchForm
from .models import BloodType, Message


def navbar(request):
    unread = 0
    if request.user.is_authenticated:
        unread = Message.objects.filter(receiver=request.user, is_read=False).count()
    return {
        "nav_search_form": SearchForm(),
        "nav_blood_types": BloodType.objects.all(),
        "unread_count": unread,
    }
