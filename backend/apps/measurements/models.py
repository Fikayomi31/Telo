from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Measurement(models.Model):

    class Unit(models.TextChoices):
        CM = "CM", "Centimetres"
        INCH = "INCH", "Inches"

    class Source(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AI = "AI", "AI Assisted"

    vendor_customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="recorded_measurements")

    chest = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hips = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shoulder = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    neck = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sleeve_length = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shirt_length = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    trouser_length = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    inseam = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.INCH)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.AI)
    ai_confidence = models.DecimalField(max_length=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Measurement for {self.vendor_customer.full_name}"
