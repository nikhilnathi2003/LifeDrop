"""Sai Srinivas Uppara — messaging, guest donation, inbox and user history."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import MessageForm, GuestOfferForm
from ..models import BloodRequest, Message, GuestOffer, UserVisit, SearchQuery


@login_required
def send_message(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if req.requester == request.user:
        messages.error(request, "You cannot message your own request.")
        return redirect("request_detail", pk=pk)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = req.requester
            msg.request = req
            msg.save()
            messages.success(request, "Message sent to the requester.")
    return redirect("request_detail", pk=pk)


@login_required
def offer_to_donate(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if req.requester == request.user:
        messages.error(request, "This is your own request.")
        return redirect("request_detail", pk=pk)
    Message.objects.create(sender=request.user, receiver=req.requester, request=req,
                           body=f"Hi, I can donate {req.blood_type} blood. Please contact me.")
    messages.success(request, "Thank you! The requester has been notified of your offer.")
    return redirect("request_detail", pk=pk)


def guest_donate(request, pk):
    """GA requirement: a guest can offer to donate WITHOUT signing in.

    No @login_required — anyone can reach this. A signed-in user is nudged to
    use the one-click offer instead, but guests just leave a name and phone.
    """
    req = get_object_or_404(BloodRequest, pk=pk)
    if request.method == "POST":
        form = GuestOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.request = req
            offer.save()
            messages.success(
                request,
                f"Thank you, {offer.name}! The family has your details and will "
                "reach out. You just helped without even making an account.")
            return redirect("request_detail", pk=pk)
    else:
        # pre-fill the blood type with the one the request needs
        form = GuestOfferForm(initial={"blood_type": req.blood_type_id})
    return render(request, "donors/guest_donate.html", {"form": form, "request_obj": req})


@login_required
def inbox(request):
    """Messages received/sent, plus guest offers on the user's own requests."""
    received = (Message.objects.filter(receiver=request.user)
                .select_related("sender", "request").order_by("-created_at"))
    sent = (Message.objects.filter(sender=request.user)
            .select_related("receiver", "request").order_by("-created_at"))
    guest_offers = (GuestOffer.objects.filter(request__requester=request.user)
                    .select_related("request", "blood_type").order_by("-created_at"))
    # mark everything addressed to me as read when I open the inbox
    received.filter(is_read=False).update(is_read=True)
    guest_offers.filter(is_read=False).update(is_read=True)
    return render(request, "donors/inbox.html",
                  {"received": received, "sent": sent, "guest_offers": guest_offers})


@login_required
def thread(request, username):
    """A full conversation between the logged-in user and another user, with reply."""
    other = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other
            msg.save()
            return redirect("thread", username=username)
    msgs = Message.objects.filter(
        Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
    ).select_related("sender", "request").order_by("created_at")
    Message.objects.filter(sender=other, receiver=request.user, is_read=False).update(is_read=True)
    return render(request, "donors/thread.html",
                  {"other": other, "msgs": msgs, "form": MessageForm()})


@login_required
def user_history(request):
    """Sessions + cookies + DB history: visits per day, recently viewed, searches."""
    visits = UserVisit.objects.filter(user=request.user).order_by("-date")[:14]
    viewed_ids = request.session.get("recently_viewed", [])
    recently_viewed = list(BloodRequest.objects.filter(id__in=viewed_ids)
                           .select_related("blood_type"))
    # keep them in the order they were viewed
    recently_viewed.sort(key=lambda r: viewed_ids.index(r.id))
    recent_searches = request.session.get("recent_searches", [])
    first_visit = request.COOKIES.get("first_visit")
    return render(request, "donors/history.html", {
        "visits": visits,
        "recently_viewed": recently_viewed,
        "recent_searches": recent_searches,
        "first_visit": first_visit,
    })
