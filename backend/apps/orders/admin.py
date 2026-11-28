from django.contrib import admin

from .models import Order, OrderItem, OrderStatusHistory, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("previous_status", "new_status", "changed_by", "note", "created_at")
    can_delete = False
    max_num = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("order_number", "vendor_customer", "status", "order_date", "expected_completion_date", "total_amount")
    list_filter = ("status", "order_date", "expected_completion_date")
    search_fields = (
        "vendor_customer__customer__full_name",
        "vendor_customer__customer__phone_number",
        "vendor_customer__vendor__business_name"
        )

    readonly_fields = ("order_number", "order_date", "created_at", "updated_at")
    inlines = [OrderItemInline, OrderStatusHistoryInline, PaymentInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item_name", "quantity", "unit_price", "total_price")
    search_fields = ("item_name", "order__vendor_customer__customer__full_name")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):

    list_display = ("order", "previous_status", "new_status", "changed_by", "created_at")
    list_filter = ("previous_status", "new_status", "created_at")

    readonly_fields = ("order", "previous_status", "new_status", "changed_by", "note", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = ("order", "amount", "method", "status", "transaction_reference", "paid_at")
    list_filter = ("method", "status", "paid_at")
    search_fields = ("transaction_reference", "order__vendor_customer__customer__full_name")

    readonly_fields = ("created_at",)
    

