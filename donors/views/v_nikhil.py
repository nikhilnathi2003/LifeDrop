"""Nikhil Goud Nathi — register, donor profile, verification, donor directory."""
import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..forms import RegisterForm, DonorProfileForm, DonorVerificationForm
from ..models import DonorProfile, BloodType

DONATION_GAP_DAYS = 56


def _eligibility(profile):
    """Return (is_eligible, next_date) based on the 56-day rule."""
    if not profile.last_donation:
        return True, None
    next_date = profile.last_donation + datetime.timedelta(days=DONATION_GAP_DAYS)
    return timezone.now().date() >= next_date, next_date


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data["email"]
            user.save()
            DonorProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Welcome to LifeDrop!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "donors/register.html", {"form": form})


@login_required
def profile(request):
    prof, _ = DonorProfile.objects.get_or_create(user=request.user)
    form = DonorProfileForm(request.POST or None, instance=prof)
    card_form = DonorVerificationForm()
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile saved.")
        return redirect("profile")
    eligible, next_date = _eligibility(prof)
    return render(request, "donors/profile.html",
                  {"form": form, "card_form": card_form, "profile": prof,
                   "eligible": eligible, "next_date": next_date})


@login_required
def upload_card(request):
    if request.method == "POST":
        form = DonorVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "Donor card uploaded. It will be reviewed shortly.")
    return redirect("profile")


def donor_directory(request):
    """Browse available donors, filter by blood type and city. Open to guests."""
    donors = (DonorProfile.objects.filter(available=True)
              .select_related("user", "blood_type"))
    bt = request.GET.get("blood_type")
    city = request.GET.get("city", "").strip()
    if bt:
        donors = donors.filter(blood_type_id=bt)
    if city:
        donors = donors.filter(city__icontains=city)
    return render(request, "donors/donor_directory.html", {
        "donors": donors,
        "blood_types": BloodType.objects.all(),
        "total": donors.count(),
    })


def donor_public(request, username):
    """A public donor profile that anyone can view."""
    user = get_object_or_404(User, username=username)
    prof = get_object_or_404(DonorProfile, user=user)
    eligible, next_date = _eligibility(prof)
    return render(request, "donors/donor_public.html",
                  {"donor": prof, "eligible": eligible, "next_date": next_date})


@login_required
def donor_dashboard(request):
    """A personal hub for the logged-in donor: profile, eligibility, activity."""
    from ..models import BloodRequest, Message
    prof, _ = DonorProfile.objects.get_or_create(user=request.user)
    eligible, next_date = _eligibility(prof)
    my_requests = BloodRequest.objects.filter(requester=request.user)
    offers_made = Message.objects.filter(sender=request.user,
                                         body__icontains="can donate").count()
    saved = len(request.session.get("saved_requests", []))
    # a friendly donor "level" based on how active they are
    points = offers_made * 10 + my_requests.count() * 5 + (20 if prof.is_verified else 0)
    if points >= 60:
        level, icon = "Gold donor", "bi-award-fill"
    elif points >= 25:
        level, icon = "Silver donor", "bi-award"
    else:
        level, icon = "New donor", "bi-star"
    return render(request, "donors/dashboard.html", {
        "profile": prof, "eligible": eligible, "next_date": next_date,
        "my_requests": my_requests, "open_count": my_requests.exclude(status="fulfilled").count(),
        "offers_made": offers_made, "saved": saved,
        "level": level, "level_icon": icon, "points": points,
    })
