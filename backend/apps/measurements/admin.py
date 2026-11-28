from django.contrib import admin

from .models import Measurement

@admin.register(Measurement)
class Measurement(admin.ModelAdmin):
    list_display = ("vendor_customer", "unit", "source", "ai_confidence", "is_verified", "created_at")
    list_filter = ("unit", "source", "is_verified", "created_at")

    search_fields = (
        "vendor_customer__customer__full_name",
        "vendor_customer__customer__phone_number",
        "vendor_customer__vendor__business_name"
    )

    readonly_fields = ("created_at",)
