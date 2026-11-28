from django.contrib import admin

from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient_type", "channel", "recipient_email", "recipient_phone", "status", "sent_at", "created_at")
    list_filter = ("recipient_type", "channel", "status", "created_at")
    search_fields = ("recipient_email", "recipient_phone", "subject", "message")

    readonly_fields = ("provider_reference", "failure_reason", "sent_at", "created_at")
