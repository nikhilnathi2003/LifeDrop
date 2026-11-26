"""Sneha Gunturu — contact, about, team, reviews, FAQ, eligibility pages."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ContactForm, ReviewForm
from ..models import BloodRequest, Review


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
        ("Sujith Chitram", "Requests, status & fixtures", "BloodType, BloodRequest"),
        ("Venkata Charan Sai Doniparthi", "Search, saved items & uploads", "RequestImage, SearchQuery"),
        ("Sneha Gunturu", "Design, pages, reviews & FAQ", "ContactMessage, Review"),
        ("Nikhil Goud Nathi", "Accounts, donor directory & auth", "DonorProfile, DonorVerification"),
        ("Sai Srinivas Uppara", "Messaging, guest donation & history", "Message, UserVisit, GuestOffer"),
    ]
    return render(request, "donors/team.html", {"members": members})


@login_required
def leave_review(request, pk):
    """Leave a star review for the person who posted a request."""
    req = get_object_or_404(BloodRequest, pk=pk)
    target = req.requester
    if target == request.user:
        messages.error(request, "You cannot review yourself.")
        return redirect("request_detail", pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.user = target
            review.save()
            messages.success(request, "Thanks for your review!")
            return redirect("request_detail", pk=pk)
    else:
        form = ReviewForm()
    return render(request, "donors/leave_review.html",
                  {"form": form, "request_obj": req, "target": target})


def faq(request):
    faqs = [
        ("Who can donate blood?",
         "Most healthy adults aged 17–65 who weigh at least 50 kg can donate. "
         "You can give whole blood once every 56 days."),
        ("Do I need an account to help?",
         "No. Thanks to guest donation you can offer to donate without signing in — "
         "just leave your name and a phone number on any request."),
        ("Is LifeDrop free?",
         "Yes. Posting a request, browsing and offering to donate are all free. "
         "We never charge patients or donors."),
        ("How does the Verified donor badge work?",
         "Upload a photo of your blood donor card on your profile. Once an admin "
         "reviews it, a Verified badge appears next to your name."),
        ("Does donating hurt or take long?",
         "The donation itself takes about 8–10 minutes; the whole visit is around "
         "45 minutes. Most people feel just a quick pinch."),
        ("How soon will someone respond to my request?",
         "Requests are shown to nearby donors immediately, and most posts get a first "
         "offer within a short time, especially for urgent and critical cases."),
    ]
    return render(request, "donors/faq.html", {"faqs": faqs})


def drives(request):
    """Upcoming blood-donation camps and events people can attend."""
    events = [
        {"title": "University of Windsor Blood Drive", "date": "Dec 5, 2026",
         "time": "10:00 – 16:00", "place": "CAW Student Centre, Windsor", "slots": 40, "urgency": "urgent"},
        {"title": "Erie Shores Community Camp", "date": "Dec 12, 2026",
         "time": "09:00 – 14:00", "place": "Erie Shores HealthCare, Leamington", "slots": 25, "urgency": "normal"},
        {"title": "Holiday Critical-Stock Drive", "date": "Dec 20, 2026",
         "time": "08:00 – 18:00", "place": "Windsor Regional Hospital", "slots": 60, "urgency": "critical"},
        {"title": "New Year Donor Meetup", "date": "Jan 3, 2027",
         "time": "11:00 – 15:00", "place": "Downtown Windsor Library", "slots": 30, "urgency": "normal"},
    ]
    return render(request, "donors/drives.html", {"events": events})


def eligibility(request):
    """Eligibility checklist + a who-can-give-to-whom compatibility table."""
    checklist = [
        ("Age 17–65", True),
        ("Weigh at least 50 kg", True),
        ("Feeling well and healthy today", True),
        ("At least 56 days since your last whole-blood donation", True),
        ("No cold, flu or fever in the last 2 weeks", True),
    ]
    compatibility = [
        ("O-", ["Everyone (universal donor)"]),
        ("O+", ["O+", "A+", "B+", "AB+"]),
        ("A-", ["A-", "A+", "AB-", "AB+"]),
        ("A+", ["A+", "AB+"]),
        ("B-", ["B-", "B+", "AB-", "AB+"]),
        ("B+", ["B+", "AB+"]),
        ("AB-", ["AB-", "AB+"]),
        ("AB+", ["AB+ only"]),
    ]
    return render(request, "donors/eligibility.html",
                  {"checklist": checklist, "compatibility": compatibility})
