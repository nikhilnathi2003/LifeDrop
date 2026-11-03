"""Venkata Charan Sai Doniparthi — image uploads and saved requests.

Search lives in the home ListView; this file owns the image-upload view,
photo deletion, and the session-based saved-requests (bookmark) feature.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ImageForm
from ..models import BloodRequest, RequestImage

SAVED_KEY = "saved_requests"


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
    """Remove a photo from one of your own requests (owner only)."""
    img = get_object_or_404(RequestImage, pk=pk, request__requester=request.user)
    req_id = img.request_id
    if request.method == "POST":
        img.delete()
        messages.info(request, "Photo removed.")
    return redirect("request_detail", pk=req_id)


def toggle_saved(request, pk):
    """Bookmark / un-bookmark a request. Stored in the session, so guests can use it too."""
    get_object_or_404(BloodRequest, pk=pk)          # make sure it exists
    saved = request.session.get(SAVED_KEY, [])
    if pk in saved:
        saved.remove(pk)
        messages.info(request, "Removed from saved requests.")
    else:
        saved.insert(0, pk)                         # newest first
        messages.success(request, "Saved for later.")
    request.session[SAVED_KEY] = saved
    request.session.modified = True                 # tell Django the session changed
    return redirect(request.META.get("HTTP_REFERER") or "home")


def saved_requests(request):
    """Show the requests the user has bookmarked this session (kept in saved order)."""
    ids = request.session.get(SAVED_KEY, [])
    reqs = list(BloodRequest.objects.filter(pk__in=ids).select_related("blood_type"))
    reqs.sort(key=lambda r: ids.index(r.pk))
    return render(request, "donors/saved.html", {"requests": reqs})
