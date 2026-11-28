from django.contrib import admin

from .models import Design, CustomerPhoto, TryOnResult


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("title", "vendor", "category", "source", "uploaded_by", "created_at")
    list_filter = ("category", "source", "created_at")

    search_fields = ("title", "vendor__business_name", "vendor_customer__customer__full_name")
    readonly_fields = ("created_at",)

@admin.register(CustomerPhoto)
class CustomerPhotoAdmin(admin.ModelAdmin):

    list_display = ("vendor_customer", "photo_type", "uploaded_by", "created_at")
    list_filter = ("photo_type", "created_at")

    search_fields = ("vendor_customer__customer__full_name", "vendor_customer__vendor__business_name")
    readonly_fields = ("created_at",)


@admin.register(TryOnResult)
class TryOnResultAdmin(admin.ModelAdmin):

    list_display = ("vendor_customer", "design", "status", "ai_model", "created_at")
    list_filter = ("status", "ai_model", "created_at")

    search_fields = ("vendor_customer__customer__full_name", "design__title", "ai_model")
    readonly_fields = ("created_at", "updated_at")

