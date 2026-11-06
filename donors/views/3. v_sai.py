"""Sai Srinivas Uppara — messaging (message requester / offer to donate).

Remaining ~40% for this member (see README):
    - inbox(request)        : list received and sent messages
    - user_history(request) : visits/day, recently viewed, recent searches
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..forms import MessageForm
from ..models import BloodRequest, Message


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


# TODO (Sai Srinivas): inbox + user_history views to finish the messaging/history part.
