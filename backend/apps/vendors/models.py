from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class VendorProfile(models.Model):

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "pending"
        VERIFIED = "VERIFIED", "verified"
        REJECTED = "REJECTED", "Rejected"

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_profile")
    business_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    business_email = models.EmailField(blank=True)
    business_phone = models.CharField(max_length=11)
    logo = models.ImageField(upload_to="vendors/logos/", blank=True, null=True)

    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.business_name


class VendorLocation(models.Model):

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="location")
    country = models.CharField(max_length=100, default="Nigeria")
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    lga = models.CharField(max_length=50, blank=True)
    street_address = models.CharField(max_length=255)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "city"]

    def __str__(self):
        return f"{self.vendor.business_name} - {self.city}"


class VendorService(models.Model):

    class Category(models.TextChoices):
        TRADITIONAL = "TRADITIONAL", "Traditional Wear"
        SUITS = "SUITS", "Suits"
        DRESSES = "DRESSES", "Dresses"
        CASUAL = "CASUAL", "Casual Wear"
        STREETWEAR = "STREETWEAR", "Streetwear"
        OTHER = "OTHER" "Other"

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="service")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    category = models.CharField(max_length=20,choices=Category.choices, default=Category.OTHER)

    base_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    currency = models.CharField(max_length=3, default="NGN")
    estimated_day = models.PositiveSmallIntegerField(default=7)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["vendors", "name"], name="unique_vendor_service_name")]

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"
    