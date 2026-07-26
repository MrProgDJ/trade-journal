import json
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count, Avg, Q

from .models import Trade
from .forms import TradeForm, RegisterForm, TradeFilterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'journal/register.html', {'form': form})


@login_required
def dashboard(request):
    trades = Trade.objects.filter(user=request.user)

    total_trades = trades.count()
    # Calculate wins manually
    win_count = sum(1 for t in trades if t.pnl > 0)
    win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0

    total_pnl = sum(t.pnl for t in trades)
    total_pnl_pct = sum(t.pnl_percentage for t in trades) / total_trades if total_trades > 0 else 0

    best_trade = trades.order_by('-pnl').first() if total_trades > 0 else None
    worst_trade = trades.order_by('pnl').first() if total_trades > 0 else None

    # Recent trades
    recent_trades = trades[:5]

    # Monthly summary
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_trades = trades.filter(date__gte=month_start.date())
    monthly_pnl = sum(t.pnl for t in monthly_trades)

    # Weekly stats
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    weekly_trades = trades.filter(date__gte=week_start.date())
    weekly_pnl = sum(t.pnl for t in weekly_trades)

    context = {
        'total_trades': total_trades,
        'win_rate': round(win_rate, 1),
        'total_pnl': round(total_pnl, 2),
        'total_pnl_pct': round(total_pnl_pct, 2),
        'best_trade': best_trade,
        'worst_trade': worst_trade,
        'recent_trades': recent_trades,
        'monthly_pnl': round(monthly_pnl, 2),
        'monthly_trades_count': monthly_trades.count(),
        'weekly_pnl': round(weekly_pnl, 2),
        'weekly_trades_count': weekly_trades.count(),
    }
    return render(request, 'journal/dashboard.html', context)


@login_required
def trade_list(request):
    trades = Trade.objects.filter(user=request.user)
    form = TradeFilterForm(request.GET)

    if form.is_valid():
        symbol = form.cleaned_data.get('symbol')
        side = form.cleaned_data.get('side')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if symbol:
            trades = trades.filter(symbol__icontains=symbol)
        if side:
            trades = trades.filter(side=side)
        if date_from:
            trades = trades.filter(date__gte=date_from)
        if date_to:
            trades = trades.filter(date__lte=date_to)

    # Calculate totals for filtered trades
    filtered_trades = list(trades)
    total_pnl = sum(t.pnl for t in filtered_trades)
    total_count = len(filtered_trades)
    win_count = sum(1 for t in filtered_trades if t.pnl > 0)
    win_rate = (win_count / total_count * 100) if total_count > 0 else 0

    context = {
        'trades': trades,
        'filter_form': form,
        'total_pnl': round(total_pnl, 2),
        'total_count': total_count,
        'win_count': win_count,
        'win_rate': round(win_rate, 1),
    }
    return render(request, 'journal/trade_list.html', context)


@login_required
def trade_add(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect('trade_list')
    else:
        form = TradeForm()
    return render(request, 'journal/trade_form.html', {'form': form, 'title': 'Add Trade / افزودن معامله'})


@login_required
def trade_edit(request, pk):
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TradeForm(request.POST, instance=trade)
        if form.is_valid():
            form.save()
            return redirect('trade_list')
    else:
        form = TradeForm(instance=trade)
    return render(request, 'journal/trade_form.html', {'form': form, 'title': 'Edit Trade / ویرایش معامله', 'trade': trade})


@login_required
def trade_delete(request, pk):
    trade = get_object_or_404(Trade, pk=pk, user=request.user)
    if request.method == 'POST':
        trade.delete()
        return redirect('trade_list')
    return render(request, 'journal/trade_confirm_delete.html', {'trade': trade})


@login_required
def trades_chart_data(request):
    """API endpoint for Chart.js data."""
    trades = Trade.objects.filter(user=request.user).order_by('date')

    cumulative_pnl = 0
    labels = []
    pnl_data = []
    cumulative_data = []

    for trade in trades:
        labels.append(trade.date.strftime('%Y-%m-%d'))
        pnl_data.append(round(trade.pnl, 2))
        cumulative_pnl += trade.pnl
        cumulative_data.append(round(cumulative_pnl, 2))

    return JsonResponse({
        'labels': labels,
        'pnl': pnl_data,
        'cumulative': cumulative_data,
    })
