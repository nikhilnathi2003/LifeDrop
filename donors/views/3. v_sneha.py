"""Sneha Gunturu — contact, about, team pages."""
from django.contrib import messages
from django.shortcuts import redirect, render

from ..forms import ContactForm


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks! We'll get back to you.")
        return redirect("contact")
    return render(request, "donors/contact.html", {"form": form})


def about(request):
    return render(request, "donors/about.html")


def team(request):
    members = [
        ("Sujith Chitram", "Requests & fixtures", "BloodType, BloodRequest"),
        ("Venkata Charan Sai Doniparthi", "Search & image uploads", "RequestImage, SearchQuery"),
        ("Sneha Gunturu", "Design, footer, pages", "ContactMessage, Review"),
        ("Nikhil Goud Nathi", "Accounts & auth", "DonorProfile, DonorVerification"),
        ("Sai Srinivas Uppara", "Messaging & user history", "Message, UserVisit"),
    ]
    return render(request, "donors/team.html", {"members": members})
