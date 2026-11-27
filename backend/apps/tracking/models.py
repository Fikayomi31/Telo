from django.db import models

import uuid

class TrackingReference(models.Model):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="tracking_reference")
    tracking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tracking_code)


class TrackingVerification(models.Model):

    tracking_reference = models.ForeignKey(TrackingReference, on_delete=models.CASCADE, related_name="verification_attempts")
    otp_hash = models.CharField(max_length=255)
    expired_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Verification for {self.tracking_reference.tracking_code}"
