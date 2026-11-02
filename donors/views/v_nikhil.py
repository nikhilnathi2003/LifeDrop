"""Nikhil Goud Nathi — register, donor profile, donor-card verification."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import RegisterForm, DonorProfileForm, DonorVerificationForm
from ..models import DonorProfile


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
    return render(request, "donors/profile.html",
                  {"form": form, "card_form": card_form, "profile": prof})


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
