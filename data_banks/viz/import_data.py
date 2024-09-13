import pandas as pd
from .models import *

def import_ownership(dataframe):
    for index, row in dataframe.iterrows():
        Ownership.objects.create(
            symbol=row['symbol'],
            company_name=row['company_name'] ,
            ownership_name=row['name'],
            share_value=row['share_value'],
            share_amount=row['share_amount'],
            share_percentage=row['share_percentage']
        )

def import_historicalfinancial(dataframe):
    for index, row in dataframe.iterrows():
        HistoricalFinancials.objects.create(
            symbol=row['symbol'], 
            company_name=row['company_name'],
            year=row['year'],
            tax=row['tax'], 
            revenue=row['revenue'], 
            earnings=row['earnings'],
            cash_only=row['cash_only'], 
            total_debt=row['total_debt'], 
            fixed_assets=row['fixed_assets'], 
            total_equity=row['total_equity'], 
            operating_pnl=row['operating_pnl'], 
            total_liabilities=row['total_liabilities'], 
            current_liabilities=row['current_liabilities'], 
            earnings_before_tax=row['earnings_before_tax'], 
            cash_and_equivalents=row['cash_and_equivalents'], 
            total_cash_and_due_from_banks=row['total_cash_and_due_from_banks'],
            gross_profit=row['gross_profit'],
            total_assets=row['total_assets']
        )

def import_historical_valuation(dataframe):
    for index, row in dataframe.iterrows():
        Historical_Valuation.objects.create(
            symbol = row['symbol'],
            company_name = row['company_name'],
            year = row['year'],
            pb = row['pb'],
            pe = row['pe'],
            ps = row['ps'],
            pb_peer_avg = row['pb_peer_avg'],
            pe_peer_avg = row['pe_peer_avg'],
            ps_peer_avg = row['ps_peer_avg']
        )      

def import_overview(dataframe):
    for index, row in dataframe.iterrows():
        Overview.objects.create(
            symbol = row['symbol'],
            company_name = row['company_name'],
            listing_board = row['overview.listing_board'],
            industry = row['overview.industry'],
            sub_industry = row['overview.sub_industry'],
            sector = row['overview.sector'],
            sub_sector = row['overview.sub_sector'],
            market_cap = row['overview.market_cap'],
            market_cap_rank = row['overview.market_cap_rank'],
            address = row['overview.address'],
            employee_num = row['overview.employee_num'],
            listing_date = row['overview.listing_date'],
            website = row['overview.website'],
            phone = row['overview.phone'],
            email = row['overview.email'],
            last_close_price = row['overview.last_close_price'],
            latest_close_date = row['overview.latest_close_date'],
            daily_close_change = row['overview.daily_close_change']
        )

def run():
    #ownership
    ownership_file_path = "../ownership_banks.csv"
    ownership_df = pd.read_csv(ownership_file_path)
    ownership_df = ownership_df.dropna(axis=0)

    import_ownership(ownership_df)

    #historicalfinancial
    historicalfinancial_file_path = "../historicalfinancial.csv"
    historicalfinancial_df = pd.read_csv(historicalfinancial_file_path)

    import_historicalfinancial(historicalfinancial_df)

    #historical_valuation
    historical_valuation_file_path = "../historicalvaluation.csv"
    historical_valuation_df = pd.read_csv(historical_valuation_file_path)
    
    import_historical_valuation(historical_valuation_df)

    #overview
    overview_file_path = "../overview.csv"
    overview_df = pd.read_csv(overview_file_path)
    
    import_overview(overview_df)


