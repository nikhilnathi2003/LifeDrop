"""Venkata Charan Sai Doniparthi — image uploads, saved requests, search history."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Count, IntegerField, When
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ImageForm
from ..models import BloodRequest, RequestImage, SearchQuery, BloodType


@login_required
def upload_images(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.request = req
            img.save()
            messages.success(request, "Photo added.")
            return redirect("request_detail", pk=pk)
    else:
        form = ImageForm()
    return render(request, "donors/upload_images.html", {"form": form, "request_obj": req})


@login_required
def delete_image(request, pk):
    """Owner removes a photo from one of their requests."""
    img = get_object_or_404(RequestImage, pk=pk, request__requester=request.user)
    req_pk = img.request_id
    img.delete()
    messages.success(request, "Photo removed.")
    return redirect("request_detail", pk=req_pk)


def toggle_save(request, pk):
    """Bookmark / un-bookmark a request. Works for guests too (session based)."""
    get_object_or_404(BloodRequest, pk=pk)
    saved = request.session.get("saved_requests", [])
    if pk in saved:
        saved.remove(pk)
        messages.info(request, "Removed from your saved requests.")
    else:
        saved.insert(0, pk)
        messages.success(request, "Saved. Find it under 'Saved requests'.")
    request.session["saved_requests"] = saved
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER") or "home")


def saved_requests(request):
    """Show the requests the visitor bookmarked (kept in the session)."""
    saved_ids = request.session.get("saved_requests", [])
    reqs = list(BloodRequest.objects.filter(id__in=saved_ids).select_related("blood_type"))
    reqs.sort(key=lambda r: saved_ids.index(r.id))
    return render(request, "donors/saved_requests.html", {"requests": reqs})


def advanced_search(request):
    """A fuller search page: blood type + city + urgency + sort, plus popular types."""
    qs = BloodRequest.objects.exclude(status="fulfilled").select_related("blood_type")
    bt = request.GET.get("blood_type")
    city = request.GET.get("city", "").strip()
    urg = request.GET.get("urgency")
    sort = request.GET.get("sort", "new")
    if bt:
        qs = qs.filter(blood_type_id=bt)
    if city:
        qs = qs.filter(city__icontains=city)
    if urg in ("normal", "urgent", "critical"):
        qs = qs.filter(urgency=urg)
    if sort == "urgency":
        qs = qs.annotate(rank=Case(
            When(urgency="critical", then=0),
            When(urgency="urgent", then=1),
            default=2, output_field=IntegerField())).order_by("rank", "-created_at")
    else:
        qs = qs.order_by("-created_at")
    popular = (SearchQuery.objects.filter(blood_type__isnull=False)
               .values("blood_type__name").annotate(n=Count("id")).order_by("-n")[:6])
    return render(request, "donors/advanced_search.html", {
        "results": qs, "blood_types": BloodType.objects.all(),
        "popular": popular, "total": qs.count(),
    })


def recent_searches(request):
    """A page of the searches run recently (DB for members, session for all)."""
    db_searches = []
    if request.user.is_authenticated:
        db_searches = (SearchQuery.objects.filter(user=request.user)
                       .select_related("blood_type")[:20])
    session_searches = request.session.get("recent_searches", [])
    return render(request, "donors/recent_searches.html",
                  {"db_searches": db_searches, "session_searches": session_searches})
