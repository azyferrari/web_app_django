from django.urls import path
from .views import *

urlpatterns = [
    # url for chart
    path('home/', HomeView.as_view(), name='home'),
    path('historicalfinancials/', historicalfinancialsView.as_view(), name='historicalfinancials'),
    path('historicalvaluation/', HistoricalValuationView.as_view(), name='historicalvaluation'),
    path('overview/', OverviewView.as_view(), name='overview'),

    # url for login, logout, register
    path('login/', login.as_view(), name='login'),
    path('logout/', logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # url for cache
    path('ownership-cache', ownership_cache.as_view(), name='ownership-cache'),
    path('hist-financial-cache', hist_financial_cache.as_view(), name='hist-financial-cache'),
    path('hist-valuation-cache', hist_valuation_cache.as_view(), name='hist-valuation-cache'),
    path('overview-cache', overview_cache.as_view(), name='overview-cache'),
]