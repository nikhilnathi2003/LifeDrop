from django.contrib import admin

from .models import (BloodType, BloodRequest, RequestImage, SearchQuery,
                     ContactMessage, Review, DonorProfile, DonorVerification,
                     Message, UserVisit)


class RequestImageInline(admin.TabularInline):
    model = RequestImage
    extra = 1


@admin.register(BloodType)
class BloodTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("patient", "blood_type", "hospital", "city", "units", "urgency", "status", "created_at")
    list_filter = ("blood_type", "urgency", "status", "city")
    search_fields = ("patient", "hospital", "notes")
    inlines = [RequestImageInline]


@admin.register(DonorVerification)
class DonorVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "submitted_at")
    list_filter = ("status",)
    actions = ["approve_selected"]

    @admin.action(description="Approve selected donor cards")
    def approve_selected(self, request, queryset):
        queryset.update(status="approved")


admin.site.register(RequestImage)
admin.site.register(SearchQuery)
admin.site.register(ContactMessage)
admin.site.register(Review)
admin.site.register(DonorProfile)
admin.site.register(Message)
admin.site.register(UserVisit)
