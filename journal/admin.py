from django.contrib import admin
from .models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'side', 'entry_price', 'exit_price', 'quantity', 'date', 'pnl', 'user']
    list_filter = ['side', 'date', 'user']
    search_fields = ['symbol', 'notes']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']
