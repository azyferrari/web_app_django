import json
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.generics import ListAPIView 
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from .forms import SignUpForm
from .models import *
from .serializers import *

"""
class for get data to visualize
"""

class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        # Get data top 5 banks by share value
        top_5_share_values = (Ownership.objects
            .values('symbol', 'company_name') 
            .annotate(total_share_value=Sum('share_value'))  
            .order_by('-total_share_value')[:5])
        
        # Get data top 5 banks by share amount
        top_5_share_amount = (Ownership.objects
            .values('symbol', 'company_name') 
            .annotate(total_share_amount=Sum('share_amount'))  
            .order_by('-total_share_amount')[:5])
        
        # Get data share percentage each bank by top 5 share value
        company_details = {}
        for company in top_5_share_values:
            symbol = company['symbol']
            company_name = company['company_name']
            details = (Ownership.objects
                .filter(symbol=symbol)
                .values('ownership_name', 'share_percentage') 
                .order_by('-share_percentage')[:5])
        
            formatted_details = [
            {
                'ownership_name': detail['ownership_name'],
                'x': idx,  
                'y': detail['share_percentage'],  
                'r': detail['share_percentage'] * 100  
            }
            
            for idx, detail in enumerate(details, start=1)
            ]

            company_details[company_name] = list(formatted_details)  
        
        # Serialize the company_details to JSON
        company_details_json = json.dumps(company_details)

        # Get default company
        default_company = top_5_share_values[0]['company_name']

        # Prepare data for Chart.js
        context = {
            'labels_value': json.dumps([record['company_name'] for record in top_5_share_values]),
            'share_values': json.dumps([record['total_share_value'] for record in top_5_share_values]),
            'labels_amount': json.dumps([record['company_name'] for record in top_5_share_amount]),
            'share_amount': json.dumps([record['total_share_amount'] for record in top_5_share_amount]),
            'company_details_json': company_details_json,
            'company_names': json.dumps([record['company_name'] for record in top_5_share_values]),
            'default_company': default_company
        }

        return render(request, self.template_name, context)

class historicalfinancialsView(View):
    template_name = 'home/historicalfinancials.html'

    def get(self, request):
        # Get data top 5 banks by total aset
        top_5_total_assets = (HistoricalFinancials.objects
            .values('symbol', 'company_name')
            .annotate(total_total_assets=Sum('total_assets'))
            .order_by('-total_total_assets')[:5])
        
        selected_symbol = request.GET.get('symbol', top_5_total_assets[0]['symbol'])

        valuations = HistoricalFinancials.objects.filter(symbol=selected_symbol).values('year', 'revenue', 'earnings', 'total_equity', 'total_liabilities')

        years = []
        revenue_values = []
        earnings_values = []
        total_equity_values = []
        total_liabilities_values = []
        for valuation in valuations:
            years.append(valuation['year'])
            revenue_values.append(valuation['revenue'])
            earnings_values.append(valuation['earnings'])
            total_equity_values.append(valuation['total_equity'])
            total_liabilities_values.append(valuation['total_liabilities'])

        company_data = {
            'years': years,
            'revenue': revenue_values,
            'earnings': earnings_values,
            'total_equity': total_equity_values,
            'total_liabilities': total_liabilities_values
        }

        # Prepare data for Chart.js
        context = {
            'company_data': json.dumps(company_data),
            'top_5_companies': top_5_total_assets, 
            'selected_symbol': selected_symbol,    
        }

        return render(request, self.template_name, context)

class HistoricalValuationView(View):
    template_name = 'home/historicalvaluation.html'

    def get(self, request):
        top_5_total_assets = (HistoricalFinancials.objects
            .values('symbol', 'company_name')
            .annotate(total_total_assets=Sum('total_assets'))
            .order_by('-total_total_assets')[:5])

        selected_metric = request.GET.get('metric', 'pb')  

        company_data = {}
        for company in top_5_total_assets:
            symbol = company['symbol']
            company_name = company['company_name']

            valuations = HistoricalValuation.objects.filter(symbol=symbol).values('year', selected_metric)
           
            years = []
            values = []
            for valuation in valuations:
                years.append(valuation['year'])
                values.append(valuation[selected_metric])

            company_data[company_name] = {
                'years': years,
                'values': values
            }

        # Prepare data for Chart.js
        context = {
            'company_data': json.dumps(company_data),
            'metrics': ['pb', 'pe', 'ps'], 
            'selected_metric': selected_metric,
            'top_5_companies': top_5_total_assets, 
        }

        return render(request, self.template_name, context)

class OverviewView(View):
    template_name = 'home/overview.html'

    def get(self, request):
        # # Get data top 5 banks by market cap
        top_5_market_cap = (Overview.objects
            .values('symbol', 'company_name') 
            .annotate(total_market_cap=Sum('market_cap'))
            .order_by('-total_market_cap')[:5])
        
        # # Get data top 5 banks by employee num
        top_5_employee_num = (Overview.objects
            .values('symbol', 'company_name') 
            .annotate(total_employee_num=Sum('employee_num'))
            .order_by('-total_employee_num')[:5])
        
        # Prepare data for Chart.js
        context = {
            'labels_market_cap': json.dumps([record['company_name'] for record in top_5_market_cap]),
            'market_cap': json.dumps([record['total_market_cap'] for record in top_5_market_cap]),
            'labels_employee_num': json.dumps([record['company_name'] for record in top_5_employee_num]),
            'employee_num': json.dumps([record['total_employee_num'] for record in top_5_employee_num]),
        }

        return render(request, self.template_name, context)

"""
Set up a login, logout, and register
"""

class login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class logout(LogoutView):
    template_name = 'accounts/login.html'
    next_page = 'login'

class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
        return render(request, self.template_name, {'form': form})


"""
set up for caching
"""

# cache ownership
class ownership_cache(ListAPIView):
    queryset = Ownership.objects.all()
    serializer_class = OwnershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, symbol=None):
        queryset = super().get_queryset()
        if symbol:
            symbol_list = symbol.split(',')
            queryset = queryset.filter(symbol__in=symbol_list)
        return queryset
    
    def list(self, request):
        symbol = self.request.query_params.get('symbol', None)
        cache_key = f"ownership:{symbol}"
        result = cache.get(cache_key) 

        if not result: 
            print('Hitting DB') 
            result = self.get_queryset(symbol)
            print(result.values())  
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache Ownership Retrieved!')  
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)
    
# cache financials
class hist_financial_cache(ListAPIView):
    queryset = HistoricalFinancials.objects.all()
    serializer_class = HistoricalFinancialsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, symbol=None):
        queryset = super().get_queryset()
        if symbol:
            symbol_list = symbol.split(',')
            queryset = queryset.filter(symbol__in=symbol_list)
        return queryset
    
    def list(self, request):
        symbol = self.request.query_params.get('symbol', None)
        cache_key = f"historical-financials:{symbol}"
        result = cache.get(cache_key) 

        if not result: 
            print('Hitting DB') 
            result = self.get_queryset(symbol)
            print(result.values())  
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache Historical Financials Retrieved!')  
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)
    
# cache valuation
class hist_valuation_cache(ListAPIView):
    queryset = HistoricalValuation.objects.all()
    serializer_class = HistoricalValuationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, symbol=None):
        queryset = super().get_queryset()
        if symbol:
            symbol_list = symbol.split(',')
            queryset = queryset.filter(symbol__in=symbol_list)
        return queryset
    
    def list(self, request):
        symbol = self.request.query_params.get('symbol', None)
        cache_key = f"historical-valuation:{symbol}"
        result = cache.get(cache_key) 

        if not result: 
            print('Hitting DB') 
            result = self.get_queryset(symbol)
            print(result.values())  
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache Historical Valuation Retrieved!')  
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)
    
# cache overview
class overview_cache(ListAPIView):
    queryset = Overview.objects.all()
    serializer_class = OverviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, symbol=None):
        queryset = super().get_queryset()
        if symbol:
            symbol_list = symbol.split(',')
            queryset = queryset.filter(symbol__in=symbol_list)
        return queryset
    
    def list(self, request):
        symbol = self.request.query_params.get('symbol', None)
        cache_key = f"overview-cache:{symbol}"
        result = cache.get(cache_key) 

        if not result: 
            print('Hitting DB') 
            result = self.get_queryset(symbol)
            print(result.values())  
            
            cache.set(cache_key, result, 60)  
        else:
            print('Cache Overview Retrieved!')  
        
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)