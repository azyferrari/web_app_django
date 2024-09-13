import os
import requests
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()

SECTORS_API_KEY = os.getenv("SECTORS_API_KEY")
headers = {"Authorization": SECTORS_API_KEY}
base_url = "https://api.sectors.app/v1/company/report/"

sections = ["valuation"]

def banks():
    """
    Fetches the data of banks name from the specified URL and returns it as a array.
    """
    url_banks = "https://api.sectors.app/v1/companies/?sub_industry=banks"
    try:
        response_banks = requests.get(url_banks, headers=headers)
        response_banks.raise_for_status()  # Raise an exception for HTTP errors
        banks_name = response_banks.json()
        banks_name = [item['symbol'] for item in banks_name]
        return banks_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while fetching the data banks."}

def fetch_data(url):
    """
    Fetches the data from the specified URL and returns it as a JSON object.
    """
    try:
        time.sleep(5)
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An error occurred while fetching the data."}

def create_df(banks, sections, save_to_csv=False, historicalvaluation_file_name="historicalvaluation.csv"):
    """
    Creates a DataFrame by fetching data from the API for each bank in the list.

    Parameters:
    - banks: List of bank identifiers.
    - sections : List of sections.
    - save_to_csv: Boolean flag to indicate if the DataFrame should be saved to a CSV file.
    - ownership_file_name: Name of the CSV file to save the ownership section DataFrame (default is "data.csv").
    - management_file_name: Name of the CSV file to save the management section DataFrame (default is "data.csv").

    Returns:
    - DataFrame with ownership data and management data from banks of Indonesia
    """

    df_list_historicalvaluation = []
    
    for bank in banks():
        df_list=[]
        for section in sections: 
            url = f"{base_url}{bank}/?sections={section}"
            response = fetch_data(url)
            df_list.append(response)

        if "error" not in df_list:
            df = pd.json_normalize(df_list)
            #print(df.columns)
            if "valuation.historical_valuation" in df.columns:
                historicalvaluation_df = pd.json_normalize(df["valuation.historical_valuation"].explode())
                print(historicalvaluation_df)
                historicalvaluation_df["symbol"] = df["symbol"][0]
                historicalvaluation_df["company_name"] = df["company_name"][0]
                historicalvaluation_df = historicalvaluation_df.reindex(columns=
                    ['symbol', 'company_name', 'year', 'pb', 'pe', 'ps', 'pb_peer_avg', 'pe_peer_avg', 'ps_peer_avg']
                )

            df_list_historicalvaluation.append(historicalvaluation_df) 
               
        else:
            print(f"Error fetching data for {bank}")


    if not df_list_historicalvaluation:
        historicalvaluation_joined = pd.DataFrame()
    else:
        historicalvaluation_joined = pd.concat(df_list_historicalvaluation, ignore_index=True)

    if save_to_csv:
        historicalvaluation_joined.to_csv(historicalvaluation_file_name, index=False)
        print(f"Data saved to {historicalvaluation_file_name}")
        
    return historicalvaluation_joined

df = create_df(banks, sections, save_to_csv=True, historicalvaluation_file_name="historicalvaluation.csv")