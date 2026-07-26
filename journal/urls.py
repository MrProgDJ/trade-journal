from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('trades/', views.trade_list, name='trade_list'),
    path('trades/add/', views.trade_add, name='trade_add'),
    path('trades/<int:pk>/edit/', views.trade_edit, name='trade_edit'),
    path('trades/<int:pk>/delete/', views.trade_delete, name='trade_delete'),
    path('api/trades-data/', views.trades_chart_data, name='trades_chart_data'),
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
