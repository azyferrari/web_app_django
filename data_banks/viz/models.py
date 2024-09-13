from django.db import models
import math

class Ownership(models.Model):
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=200)
    ownership_name = models.CharField(max_length=200)
    share_value = models.BigIntegerField()
    share_amount = models.BigIntegerField()
    share_percentage = models.FloatField()
    
    class Meta:
         db_table = 'viz_ownership' 

class HistoricalFinancials(models.Model):
    symbol = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    earnings = models.FloatField(blank=True, null=True)
    cash_only = models.FloatField(blank=True, null=True)
    total_debt = models.FloatField(blank=True, null=True)
    fixed_assets = models.IntegerField(blank=True, null=True)
    gross_profit = models.FloatField(blank=True, null=True)
    total_assets = models.IntegerField(blank=True, null=True)
    total_equity = models.IntegerField(blank=True, null=True)
    operating_pnl = models.FloatField(blank=True, null=True)
    total_liabilities = models.IntegerField(blank=True, null=True)
    current_liabilities = models.IntegerField(blank=True, null=True)
    earnings_before_tax = models.IntegerField(blank=True, null=True)
    cash_and_equivalents = models.IntegerField(blank=True, null=True)
    total_cash_and_due_from_banks = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        float_fields = ['tax', 'earnings', 'cash_only', 'total_debt', 
                        'fixed_assets', 'operating_pnl', 'current_liabilities', 
                        'cash_and_equivalents', 'total_cash_and_due_from_banks', 
                        'gross_profit', 'total_assets']
        
        for field in float_fields:
            value = getattr(self, field)
            if isinstance(value, float) and math.isnan(value):
                setattr(self, field, None)

        super(HistoricalFinancials, self).save(*args, **kwargs)

    class Meta:
        db_table = 'viz_historical_financials'

class HistoricalValuation(models.Model):
    symbol = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    ps = models.FloatField(blank=True, null=True)
    pb_peer_avg = models.FloatField(blank=True, null=True)
    pe_peer_avg = models.FloatField(blank=True, null=True)
    ps_peer_avg = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'viz_historical_valuation'

class Overview(models.Model):
    symbol = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    listing_board = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    sub_industry = models.CharField(max_length=50, blank=True, null=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    sub_sector = models.CharField(max_length=50, blank=True, null=True)
    market_cap = models.IntegerField(blank=True, null=True)
    market_cap_rank = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    employee_num = models.IntegerField(blank=True, null=True)
    listing_date = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    last_close_price = models.IntegerField(blank=True, null=True)
    latest_close_date = models.CharField(max_length=50, blank=True, null=True) 
    daily_close_change = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'viz_overview'