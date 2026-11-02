"""Venkata Charan Sai Doniparthi — image uploads (search lives in the list view)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ImageForm
from ..models import BloodRequest


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
