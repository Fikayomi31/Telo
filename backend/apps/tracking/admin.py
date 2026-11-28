from django.contrib import admin

from .models import TrackingReference, TrackingVerification


class TrackingVerificationInline(admin.TabularInline)
    model = TrackingVerification
    extra = 0
    readonly_fields = ("otp_hash", "expires_at", "attempts", "verified_at", "created_at",)
    can_delete = False
    max_num = 0

@admin.register(TrackingReference)
class TrackingReferenceAdmin(admin.ModelAdmin):
    list_display = ("tracking_code", "order", "is_active", "expires_at", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("tracking_code", "order__vendor_customer__customer__full_name")

    readonly_fields = ("tracking_code", "created_at")
    inlines = [TrackingVerificationInline]


@admin.register(TrackingVerification)
class TrackingVerificationAdmin(admin.ModelAdmin):
    list_display = ("tracking_reference", "attempts", "expires_at", "verified_at", "created_at")
    list_filter = ("verified_at", "created_at")

    readonly_fields = ("tracking_reference", "otp_hash", "expires_at", "attempts", "verified_at", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False