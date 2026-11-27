from django.db import models
from django.conf import settings


class Design(models.Model):

    class Category(models.TextChoices):
        SHIRT = "SHIRT", "Shirt"
        TROUSER = "TROUSER", "Trousers"
        DRESS = "DRESS" "Dress"
        SUIT = "SUIT", "Suit"
        TRADITIONAL = "TRADITIONAL", "Traditional Wear"
        STREETWEAR = "STREETWEAR", "Streetwear"
        OTHER = "OTHER", "Other"

    class Source(models.TextChoices):
        VENDOR = "VENDOR", "Vendor Uploaded"
        CUSTOMER = "CUSTOMER", "Customer Provided"

    vendor = models.ForeignKey("vendors.VendorProfile", on_delete=models.CASCADE, related_name="designs")
    vendor_customer = models.ForeignKey("customers.VendorCustomer", on_delete=models.SET_NULL, null=True, blank=True, related_name="designs")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="uploaded_designs")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    image = models.ImageField(upload_to="designs/")
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.VENDOR)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CustomerPhoto(models.Model):

    class PhotoType(models.TextChoices):
        FRONT = "FRONT", "Front View"
        SIDE = "SIDE", "Side View"
        BACK = "BACK", "Back View"
        OTHER = "OTHER" "Other View"

    vendor_customer = models.ForeignKey("customer.VendorCustomer", on_delete=models.CASCADE, related_name="photos")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="uploaded_customer_phones")
    image = models.ImageField(upload_to="customer_photos/")
    photo_type = models.CharField(max_length=10, choices=PhotoType.choices, default=PhotoType.FRONT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo of {self.vendor_customer.customer.full_name}'

class TryOnResult(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    vendor_customer = models.ForeignKey("customers.VendorCustomer", on_delete=models.CASCADE, related_name="try_on_results")
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name="try_on_results")
    customer_photo = models.ForeignKey(CustomerPhoto, on_delete=models.CASCADE, related_name="try_on_results")
    generated_image = models.ImageField(upload_to="try_on_results/", blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    ai_model = models.CharField(max_length=150, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Try-on result {self.id} - {self.status}"


 
