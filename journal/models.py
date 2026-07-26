from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Trade(models.Model):
    SIDE_CHOICES = [
        ('buy', 'Buy / خرید'),
        ('sell', 'Sell / فروش'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    symbol = models.CharField('Symbol / نماد', max_length=20)
    side = models.CharField('Side / جهت', max_length=4, choices=SIDE_CHOICES)
    entry_price = models.DecimalField('Entry Price / قیمت ورود', max_digits=12, decimal_places=4)
    exit_price = models.DecimalField('Exit Price / قیمت خروج', max_digits=12, decimal_places=4)
    quantity = models.DecimalField('Quantity / تعداد', max_digits=12, decimal_places=4)
    date = models.DateField('Date / تاریخ', default=timezone.now)
    notes = models.TextField('Notes / یادداشت', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Trade / معامله'
        verbose_name_plural = 'Trades / معاملات'

    def __str__(self):
        return f"{self.symbol} {self.get_side_display()} @ {self.entry_price}"

    @property
    def pnl(self):
        """Calculate Profit & Loss."""
        if self.side == 'buy':
            return float((self.exit_price - self.entry_price) * self.quantity)
        else:
            return float((self.entry_price - self.exit_price) * self.quantity)

    @property
    def pnl_percentage(self):
        """Calculate P&L percentage."""
        if self.entry_price == 0:
            return 0
        if self.side == 'buy':
            return float(((self.exit_price - self.entry_price) / self.entry_price) * 100)
        else:
            return float(((self.entry_price - self.exit_price) / self.entry_price) * 100)

    @property
    def is_win(self):
        return self.pnl > 0
