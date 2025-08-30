from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('cardholder_name', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('cardholder_name', 'payment_intent_id')
    readonly_fields = ('payment_intent_id', 'created_at')
