from django.contrib import admin

from .models import Customer, VendorCustomer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number", "created_at")
    search_fields = ("full_name", "email")

    readonly_fields = ("created_at", "updated_at")

@admin.register(VendorCustomer)
class VendorCustomerAdmin(admin.ModelAdmin):
    list_display = ("customer", "vendor", "created_by", "is_active", "created_at")
    list_filter = ("is_active", "created_at")

    search_fields = ("customer__full_name", "vendor__business_name", "created_by__username")
    readonly_fields = ("created_at",)

