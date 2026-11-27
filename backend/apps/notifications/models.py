from django.db import models
from django.conf import settings


class Notification(models.Model):

    class RecipientType(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        TAILOR = "TAILOR", "Tailor"

    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        WHATSAPP = "WHATSAPP", "WhatsApp"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SENT = "SENT", "Sent"
        
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    recipient_type = models.CharField(max_length=10, choices=RecipientType.choices)
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=15, blank=True)
    channel = models.CharField(max_length=10, choices=Channel.choices)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    provider_reference = models.CharField(max_length=255, blank=True)
    failure_reason = models.TextField(blank=True)

    sent_at = models.DateTimeField(null=True,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel} notification - {self.status}"

    
