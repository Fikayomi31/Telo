import uuid

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        MEASUREMENT = "MEASUREMENT", "Taking Measurements"
        CUTTING = "CUTTING", "Cutting"
        SEWING = "SEWING", "Sewing"
        FITTING = "FITTING", "Fitting"
        READY = "READY", "Ready for Collection"
        COLLECTED = "COLLECTED", "Collected"
        CANCELLED = "CANCELLED", "Cancelled"

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vendor_customer = models.ForeignKey("customers.VendorCustomer", on_delete=models.PROTECT, related_name="orders")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    order_date = models.DateTimeField(auto_now_add=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    collection_date = models.DateTimeField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    design = models.ForeignKey("designs.Design", on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items")

    measurement = models.ForeignKey("measurements.Measurement", on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.item_name} - {self.order.order_number}"


class OrderStatusHistory(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    previous_status = models.CharField(max_length=20, choices=Order.Status.choices, blank=True)
    new_status = models.CharField(max_length=20, choices=Order.Status.choices)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="order_status_changes")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order.order_number} - {self.new_status}"


class Payment(models.Model):

    class Method(models.TextChoices):
        CASH = "CASH", "Cash"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
        CARD = "CARD", "Card"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=Method.choices)
    transaction_reference = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.order.order_number}"