"""Sujith Chitram — request list (index), detail, post/edit/my requests."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from ..forms import RequestForm, EditRequestForm, MessageForm
from ..models import BloodRequest, RequestImage, SearchQuery, Review
from ._helpers import track_visit, remember_recent


class RequestListView(ListView):
    model = BloodRequest
    template_name = "donors/home.html"
    context_object_name = "requests"
    paginate_by = 9

    def get_queryset(self):
        qs = BloodRequest.objects.select_related("requester", "blood_type").exclude(status="fulfilled")
        keyword = self.request.GET.get("keyword", "").strip()
        blood_type = self.request.GET.get("blood_type")
        city = self.request.GET.get("city", "").strip()
        if keyword:
            qs = qs.filter(Q(patient__icontains=keyword) | Q(hospital__icontains=keyword) | Q(notes__icontains=keyword))
        if blood_type:
            qs = qs.filter(blood_type_id=blood_type)
        if city:
            qs = qs.filter(city__icontains=city)

        if keyword or blood_type or city:
            SearchQuery.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                keyword=keyword, blood_type_id=blood_type or None)
            remember_recent(self.request, "recent_searches", keyword or city or "blood-type filter")
        return qs

    def get_context_data(self, **kwargs):
        from ..forms import SearchForm
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = SearchForm(self.request.GET or None)
        ctx["total"] = self.get_queryset().count()
        return ctx

    def get(self, request, *args, **kwargs):
        track_visit(request)
        response = super().get(request, *args, **kwargs)
        if not request.COOKIES.get("first_visit"):
            response.set_cookie("first_visit", timezone.now().date().isoformat(),
                                max_age=60 * 60 * 24 * 365)
        return response


class RequestDetailView(DetailView):
    model = BloodRequest
    template_name = "donors/request_detail.html"
    context_object_name = "request_obj"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        remember_recent(request, "recently_viewed", self.object.id)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        req = self.object
        ctx["images"] = req.images.all()
        ctx["reviews"] = Review.objects.filter(user=req.requester).select_related("reviewer")
        ctx["avg_rating"] = ctx["reviews"].aggregate(a=Avg("rating"))["a"]
        ctx["message_form"] = MessageForm()
        return ctx


@login_required
def post_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.requester = request.user
            req.save()
            if request.FILES.get("image"):
                RequestImage.objects.create(request=req, image=request.FILES["image"])
            messages.success(request, "Your blood request has been posted.")
            return redirect("request_detail", pk=req.pk)
    else:
        form = RequestForm()
    return render(request, "donors/request_form.html",
                  {"form": form, "title": "Post a blood request"})


@login_required
def edit_request(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if req.requester != request.user:
        messages.error(request, "You can only edit your own requests.")
        return redirect("request_detail", pk=pk)
    form = EditRequestForm(request.POST or None, instance=req)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Request updated.")
        return redirect("request_detail", pk=pk)
    return render(request, "donors/request_form.html", {"form": form, "title": "Edit request"})


@login_required
def my_requests(request):
    reqs = BloodRequest.objects.filter(requester=request.user)
    return render(request, "donors/my_requests.html", {"requests": reqs})
