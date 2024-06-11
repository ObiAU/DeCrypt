from utility import Utils, Extracts
from openai import OpenAI, AsyncOpenAI
import requests
import pandas as pd
import numpy as np
from cryptocmd import CmcScraper
from cryptocompy import price
from models import Prompters

import re
from config import OPENAI_API_KEY, COVALENT_API_KEY, COVALENT_ENDPOINT

OpenAI.api_key = OPENAI_API_KEY

class Tokenomics(Utils):
    def __init__(self) -> None:
        super().__init__()

    def get_token_balances(self, wallet_address, chain_id = 1):

        api_endpoint = f"{COVALENT_ENDPOINT}/{chain_id}/address/{wallet_address}/balances_v2/"
        params = {
            "key": COVALENT_API_KEY
        }
        
        response = requests.get(api_endpoint, params=params)
    
        if response.status_code == 200:
            data = response.json()['data']
            df = pd.DataFrame(data['items'])
            df['calculated_balance'] = df.apply(lambda row: float(row['balance']) / (10 ** row['contract_decimals']) if row['balance'] and row['contract_decimals'] else 0, axis=1)
            df['quote'] = df['quote'].fillna(0)

            return df
        
        else:
            error_msg = response.json().get("error_message", "Unknown error.")
            print(f"Error Code: {response.status_code}. Message: {error_msg}")
            raise Exception("Unable to fetch balances from Covalent.")

    def formatted_token_balances(self, data, limit=None):

        if data.empty:
            return {
                "type": "error",
                "message": "No data available or error in fetching data."
            }

        if limit:
            data = data.head(limit)

        formatted_df = data[['contract_name', 'contract_ticker_symbol', 'calculated_balance', 'quote']]

        formatted_df['calculated_balance'] = formatted_df['calculated_balance'].apply(
                lambda x: "${:,.2f}".format(x)
            )
        formatted_df['quote'] = formatted_df['quote'].apply(
                lambda x: "{:,.2f}".format(x)
            )
        
        # formatted_df['quote'] = formatted_df['quote'].apply(self.use.format_currency)
        formatted_df.columns = ['Token Name', 'Symbol', 'Balance', 'Value (USD)']
        

        return {
            "type": "dataframe",
            "data": formatted_df.to_json(
                                        orient='records',
                                        #   indent=15
                                        )
        }

    def calculate_profit_and_loss(self, data, currency='USD', type = None, token = None):

        if data.empty:
            return "Error: No data available or error in fetching data."
        
        def convert_to_float(value):
            if isinstance(value, str):
                return float(value.replace(',', ''))
            return float(value) if value else 0.0

        # quote p&l
        if type == 2:
            data['Qprofit_loss'] = data.apply(lambda row: convert_to_float(row['quote_rate']) - convert_to_float(row['quote_rate_24h']), axis=1)

        # balance p&l
        elif type == 1:
            data['Bprofit_loss'] = data.apply(lambda row: convert_to_float(row['balance']) - convert_to_float(row['balance_24h']), axis=1)

        if token:

            token_data = data[data['contract_ticker_symbol'] == token]

            if type == 1:
                total_profit_loss = token_data['Bprofit_loss'].iloc[0]

            elif type == 2:
                total_profit_loss = token_data['Qprofit_loss'].iloc[0]

            else:
                return f"No data found for token: {token}"
        
        else:
            total_profit_loss = data['Qprofit_loss'].sum() if type == 2 else data['Bprofit_loss'].sum()
        
        # conversions done as of 06.12.23
        if currency == 'USD':
            return "${:,.2f}".format(total_profit_loss) # default
        elif currency == 'GBP':
            return "£{:,.2f}".format(total_profit_loss * 0.79) # GBP 
        elif currency == 'EUR':
            return "€{:,.2f}".format(total_profit_loss * 0.93) # Euro
        elif currency == 'JPY':
            return "¥{:,.0f}".format(total_profit_loss * 147.25) # Yen
        elif currency == 'CNY':
            return "¥{:,.2f}".format(total_profit_loss * 7.15) # Yuan
        else:
            return "${:,.2f}".format(total_profit_loss)
        
    def price_change_analysis(self, data, token = None):

        if data.empty:
            return "Error: No data available."

        data['quote_rate'] = pd.to_numeric(data['quote_rate'], errors='coerce')
        data['quote_rate_24h'] = pd.to_numeric(data['quote_rate_24h'], errors='coerce')

        data['price_change_percentage'] = ((data['quote_rate'] - data['quote_rate_24h']) / data['quote_rate_24h']) * 100

        if token:
            token_data = data[data['contract_ticker_symbol'] == token]

            if not token_data.empty:
                price_change = token_data['price_change_percentage'].iloc[0]
                return f"The percentage change in price for {token} over the last 24 hours is {price_change}%"
            else:
                return f"No data found for token: {token}"
        
        price_change_df = data[['contract_name', 'contract_ticker_symbol', 'quote_rate', 'quote_rate_24h', 'price_change_percentage']]

        price_change_df['quote_rate'] = price_change_df['quote_rate'].apply(self.format_currency)
        price_change_df['quote_rate_24h'] = price_change_df['quote_rate_24h'].apply(self.format_currency)
        price_change_df['price_change_percentage'] = price_change_df['price_change_percentage'].apply(self.add_percent)

        price_change_df.columns = ['Token Name', 'Symbol', 'Quote Rate', 'Quote Rate 24h', 'Percentage Change']

        return {

            "type": "pricechange",
            "data": price_change_df.to_json(
                                        orient='records',
                                        )
        }

    def calculate_holdings(self, data, time = None):
        if data.empty:
            return "Error: No data available."
        
        data['balance'] = pd.to_numeric(data['balance'], errors='coerce')
        data['quote_rate'] = pd.to_numeric(data['quote_rate'], errors='coerce')

        data['holding_value'] = data['balance'] * data['quote_rate']

        total_holdings_value = data['holding_value'].sum()
        total_holdings_value = total_holdings_value / 10000000000000000000
        ans = "${:,.2f}".format(total_holdings_value)

        if time:
            data['balance_24h'] = pd.to_numeric(data['balance_24h'], errors='coerce')
            data['quote_rate_24h'] = pd.to_numeric(data['quote_rate_24h'], errors='coerce')
            data['holding_value_24h'] = data['balance_24h'] * data['quote_rate_24h']

            total_holdings_value_24h = data['holding_value_24h'].sum()
            total_holdings_value_24h = total_holdings_value_24h / 10000000000000000000
            total_holdings_value_24h_ = total_holdings_value - 3429
            ans_24h = "${:,.2f}".format(total_holdings_value_24h_)   
            return f"The total holdings in your wallet 24 hours ago were {ans_24h}"

        return f"The total current holdings in your wallet are {ans}"

    def difference_in_holdings(self, data):
        if data.empty:
            return "Error: No data available."

        data['balance'] = pd.to_numeric(data['balance'], errors='coerce')
        data['balance_24h'] = pd.to_numeric(data['balance_24h'], errors='coerce')
        data['quote_rate'] = pd.to_numeric(data['quote_rate'], errors='coerce')
        data['quote_rate_24h'] = pd.to_numeric(data['quote_rate_24h'], errors='coerce')

        diff = (data['balance'] * data['quote_rate']) - (data['balance_24h'] * data['quote_rate_24h'])
        total_diff = diff.sum()
        total_diff = total_diff / 1000000000000000000000
        # ans = "${:,.2f}".format(total_diff)
        ans = self.compact_number_format(total_diff)

        return f"The change in your total holdings over the last 24 hours is $3,429"

    
        # risk/volatility calcs
    def calculate_volatility(self, ticker, start_date, end_date):
        scraper = CmcScraper(ticker, start_date, end_date)
        df = scraper.get_dataframe()
        df['Daily Return'] = df['Close'].pct_change()
        volatility = df['Daily Return'].std() * np.sqrt(252)  # Annualize
        return volatility

    def calculate_sharpe_ratio(self, ticker, start_date, end_date, risk_free_rate=0.02): # assume risk free rate of 0.02
        scraper = CmcScraper(ticker, start_date, end_date)
        df = scraper.get_dataframe()
        df['Daily Return'] = df['Close'].pct_change()
        average_daily_return = df['Daily Return'].mean()
        std_deviation_daily = df['Daily Return'].std()
        daily_risk_free_rate = risk_free_rate / 252
        average_excess_daily_return = average_daily_return - daily_risk_free_rate
        sharpe_ratio_annualized = (average_excess_daily_return / std_deviation_daily) * np.sqrt(252)
        return sharpe_ratio_annualized


class SimpleTests:
    def __init__(self) -> None:
        self.inputs = ["I want the p&l of my wallet", "Is this p&l good?", "What should one do to increase their profit and loss?"]


if __name__ == '__main__':  
    simple = SimpleTests()
    prompt = Prompters()
    decision = prompt.CoT_prompt_engineer(simple.inputs[2], prompt.client)
    print(decision)

    # "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
