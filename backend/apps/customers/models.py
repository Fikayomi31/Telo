from django.db import models
from django.conf import settings


class Customer(models.Model):

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"

class VendorCustomer(models.Model):

    vendor = models.ForeignKey("vendors.VendorProfile", on_delete=models.CASCADE, related_name="customer_relationships")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="vendor_relationships")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="registered_customers")
    private_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["vendor", "customer"], name="unique_vendor_customer")]

    def __str__(self):
        return f"{self.customer.full_name} - {self.vendor.business_name}"
    