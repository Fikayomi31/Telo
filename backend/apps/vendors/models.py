from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class VendorProfile(models.Model):

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "pending"
        VERIFIED = "VERIFIED", "verified"
        REJECTED = "REJECTED", "Rejected"

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor profile")
    business_name = models.CharField(max_length=150)
    description = models.TextChoices(blank=True)
    business_email = models.EmailField(blank=True)
    business_phone = models.CharField(max_length=11)
    logo = models.ImageField(upload_to="vendors/logos/", blank=True, null=True)

    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.business_name
