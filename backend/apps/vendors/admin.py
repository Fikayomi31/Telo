from django.contrib import admin

from .models import VendorProfile, VendorLocation, VendorService


class VendorLocationInLine(admin.TabularInline):
    model = VendorLocation
    extra = 0

class VendorServiceInLine(admin.TabularInline):
    model = VendorService


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):

    list_display = ("business_name", "owner", "business_phone", "verification_status", "is_active", "created_at")
    list_filter = ("verification_status", "is_active", "created_at")
    search_fields = ("business_name", "owner__username", "owner__email", "business_phono")

    readonly_fields = ("created_at", "updated_at")
    inlines = [VendorLocationInLine, VendorServiceInLine]

@admin.register(VendorLocation)
class VendorLocationAdmin(admin.ModelAdmin):

    list_display = ("vendor","city", "state", "country", "is_primary")
    list_filter = ("vendor__business_name", "city", "state", "lga")

@admin.register(VendorService)
class VendorServiceAmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "category", "base_price", "currency")
    list_filter = ("category", "currency")
    search_fields = ("name", "vendor__business_name")