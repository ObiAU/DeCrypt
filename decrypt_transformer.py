import os
import asyncio
import openai
from openai import OpenAI, AsyncOpenAI
import requests
import pandas as pd
import numpy as np
from cryptocmd import CmcScraper
from cryptocompy import price
from datetime import datetime, timedelta
from dateutil import parser
from json import loads, dumps
import re
from config import OPENAI_API_KEY, COVALENT_API_KEY, COVALENT_ENDPOINT

OpenAI.api_key = OPENAI_API_KEY

def get_token_balances(wallet_address, chain_id = 1):

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

def formatted_token_balances(data, limit=None):

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
    
    # formatted_df['quote'] = formatted_df['quote'].apply(format_currency)
    formatted_df.columns = ['Token Name', 'Symbol', 'Balance', 'Value (USD)']
    

    return {
        "type": "dataframe",
        "data": formatted_df.to_json(
                                    orient='records',
                                    #   indent=15
                                      )
    }

def calculate_profit_and_loss(data, currency='USD', type = None, token = None):

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

def format_currency(value):
    return "${:,.2f}".format(value)

def add_percent(value):
    return "{:.6f}%".format(value)
    
def price_change_analysis(data, token = None):

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

    price_change_df['quote_rate'] = price_change_df['quote_rate'].apply(format_currency)
    price_change_df['quote_rate_24h'] = price_change_df['quote_rate_24h'].apply(format_currency)
    price_change_df['price_change_percentage'] = price_change_df['price_change_percentage'].apply(add_percent)

    price_change_df.columns = ['Token Name', 'Symbol', 'Quote Rate', 'Quote Rate 24h', 'Percentage Change']

    return {

        "type": "pricechange",
        "data": price_change_df.to_json(
                                    orient='records',
                                      )
    }

def calculate_holdings(data, time = None):
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

def compact_number_format(value):
    billion = 1000000000
    million = 1000000
    if abs(value) >= billion:
        return f"${value / billion:.2f}B"
    elif abs(value) >= million:
        return f"${value / million:.2f}M"
    else:
        return f"${value:,.2f}"

def difference_in_holdings(data):
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
    ans = compact_number_format(total_diff)

    return f"The change in your total holdings over the last 24 hours is $3,429"

    
def top_n_by_value(data, n):
    return data.sort_values(by='quote', ascending=False).head(n)

def top_n_by_balance(data, n):
    return data.sort_values(by='calculated_balance', ascending=False).head(n)

def filter_by_token_name(data, token_names):
    return data[data['contract_name'].isin(token_names)]

def extract_ticker(user_input):
    match = re.search(r'\b(sharpe ratio|volatility)\s+([A-Z0-9]+)', user_input.upper())
    if match:
        return match.group(2)
    else:
        raise ValueError("Ticker symbol not found in the input.")
    
    # risk/volatility calcs
def calculate_volatility(ticker, start_date, end_date):
    scraper = CmcScraper(ticker, start_date, end_date)
    df = scraper.get_dataframe()
    df['Daily Return'] = df['Close'].pct_change()
    volatility = df['Daily Return'].std() * np.sqrt(252)  # Annualize
    return volatility

def calculate_sharpe_ratio(ticker, start_date, end_date, risk_free_rate=0.02): # assume risk free rate of 0.02
    scraper = CmcScraper(ticker, start_date, end_date)
    df = scraper.get_dataframe()
    df['Daily Return'] = df['Close'].pct_change()
    average_daily_return = df['Daily Return'].mean()
    std_deviation_daily = df['Daily Return'].std()
    daily_risk_free_rate = risk_free_rate / 252
    average_excess_daily_return = average_daily_return - daily_risk_free_rate
    sharpe_ratio_annualized = (average_excess_daily_return / std_deviation_daily) * np.sqrt(252)
    return sharpe_ratio_annualized


def parse_dates_from_input(input_text):
    parts = input_text.split()
    if len(parts) != 2:
        raise ValueError("Please enter two dates in the format 'dd-mm-yyyy' or 'dd/mm/yyyy'.")

    try:
        start_date = parser.parse(parts[0], dayfirst=True).strftime('%d-%m-%Y')
        end_date = parser.parse(parts[1], dayfirst=True).strftime('%d-%m-%Y')
        return start_date, end_date
    except parser.ParserError as e:
        raise ValueError(str(e))
    
def extract_ticker(user_input, known_tickers):
    user_input = user_input.upper()
    for ticker in known_tickers:
        if ticker in user_input.split():
            return ticker
    raise ValueError("Ticker symbol not found in the input.")

def check_for_command(user_input, wallet_address, is_web=False, extra_data=None):
    try:
        commands_balance = ['token balance', 'token balances', 'token', 'tokens']
        commands_pnl = ['profit and loss', 'p&l']
        commands_sharpe = ['sharpe ratio', 'sharpe']
        commands_volatility = ['volatility', 'risk']
        known_tickers = ['BTC', 'ETH', 'XRP', 'LTC', 'ADA', 'DOGE', 'DOT', 'BCH', 'LINK', 'BNB', 'UNI', 'SOL', 'USDC', 'MANA', 'APT', 'KAKASHI']
        currency_conversions = ['GBP', 'USD', 'JPY', 'CNY', 'EUR']
        commands_holdings = ['holdings', 'balance']
        commands_price_change = ['price change', 'price', 'percentage change', 'change in percent']

        crypto_name_to_ticker = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
        }
        
        currency_name_to_symbol = {
            'british': 'GBP',
            'american': 'USD',
            'pounds': 'GBP',
            'dollars': 'USD',
            'japanese': 'JPY',
            'chinese': 'CNY',
            'yen': 'JPY',
            'euros': 'EUR',
            'european': 'EUR',
            'yuan': 'CNY',
        }

        if is_web and extra_data:
            ticker = extra_data.get("ticker")
            start_date = extra_data.get("start_date")
            end_date = extra_data.get("end_date")
        else:
            for name, ticker in crypto_name_to_ticker.items():
                user_input = user_input.replace(name, ticker)

            for currency, symbol in currency_name_to_symbol.items():
                user_input = user_input.replace(currency, symbol)

        response = get_token_balances(wallet_address)

        # unique_tickers = response['contract_ticker_symbol'].unique()
        # known_tickers.extend(ticker for ticker in unique_tickers if ticker not in known_tickers)

        if response.empty:
            return "Error: Unable to retrieve data from API."

        if "top" in user_input.lower():  
            match = re.search(r"top (\d+)", user_input.lower())
            if match:
                n = int(match.group(1))
                
                if "by value" in user_input.lower():
                    filtered_data = top_n_by_value(response, n)
                    return formatted_token_balances(filtered_data)
                
                elif "by balance" in user_input.lower():
                    filtered_data = top_n_by_balance(response, n)
                    return formatted_token_balances(filtered_data)
            else:
                return "Error: Could not find a number in your query."

        elif "token name" in user_input.lower():
            names = user_input.replace("token name", "").split(",")
            names = [name.strip() for name in names]
            filtered_data = filter_by_token_name(response, names)
            return formatted_token_balances(filtered_data)

        elif "limit" in user_input.lower():
            limit = int(user_input.split(" ")[1])
            return formatted_token_balances(response.head(limit))
        
        # token balance
        elif any(command in user_input.lower() for command in commands_balance):
            return formatted_token_balances(response)
        
        # p&l
        # elif any(command in user_input.lower() for command in currency_conversions):
        #     ans = None
        #     for curr in currency_conversions:
        #         ans = curr.lower() 
        #         return f"The profit and loss in {ans} is {calculate_profit_and_loss(response, ans)}"
            
        elif any(command in user_input.lower() for command in commands_pnl):
            
            # command_keyword = next((command for command in commands_pnl if command in user_input.lower()), None)

            selected_currency = None
            selected_token = None 
            pnl_type = None

            for currency in currency_conversions:
                if currency.lower() in user_input.lower():
                    selected_currency = currency
                    break
            
            for ticker in known_tickers:
                if ticker.lower() in user_input.lower():
                    selected_token = ticker
                    break
            
            if 'balance' in user_input.lower() or 'personal' in user_input.lower():
                pnl_type = 1
            else:
                pnl_type = 2
        

            if selected_currency:
                if selected_token:
                    pnl_result = calculate_profit_and_loss(response, selected_currency, type=pnl_type, token=selected_token)
                    return f"Sure, the profit and loss in your wallet {selected_currency} for {selected_token} over the last 24 hours is {pnl_result}"
                else:
                    pnl_result = calculate_profit_and_loss(response, selected_currency, type=pnl_type, token=None)
                    return f"Sure, the profit and loss in your wallet {selected_currency} for all tokens over the last 24 hours is {pnl_result}"
            else:
                return "Please specify the currency for the profit and loss valuation. Supported currencies: GBP, USD, JPY, CNY, EUR"
        
        # percentage change
        if any(command in user_input.lower() for command in commands_price_change):
            ptoken = None
            for ticker in known_tickers:
                if ticker.lower() in user_input.lower():
                    ptoken = ticker
                    break
            
            if ptoken:
                return price_change_analysis(response, token= ptoken)
            else:
                return price_change_analysis(response)

        # holdings calculations
        elif any(command in user_input.lower() for command in commands_holdings):
            if 'current' in user_input.lower():
                return calculate_holdings(response, time=None)
            elif 'difference' in user_input.lower() or 'change' in user_input.lower() or '24 hours' in user_input.lower() or '24h' in user_input.lower():
                return difference_in_holdings(response)
            else:
                return calculate_holdings(response, time=1)
            
            
        # sharpe ratio + risk/volatility
        elif any(command in user_input.lower() for command in commands_sharpe + commands_volatility):
            ticker = next((t for t in known_tickers if t in user_input.upper()), None)
            if ticker is None:
                return "Unknown ticker symbol."
            if ticker not in known_tickers:
                return f"Ticker symbol {ticker} is not recognized. Known tickers are: {', '.join(known_tickers)}."
                    

            if 'last year' in user_input.lower() or 'year' in user_input.lower() or '1 year' in user_input.lower():
                end_date_ = datetime.today()
                start_date_ = end_date_ - timedelta(days=365)
                end_date, start_date = end_date_.strftime("%d-%m-%Y"), start_date_.strftime("%d-%m-%Y")
            elif '6 months' in user_input.lower():
                end_date_ = datetime.today()
                start_date_ = end_date_ - timedelta(days=180)
                end_date, start_date = end_date_.strftime("%d-%m-%Y"), start_date_.strftime("%d-%m-%Y")
            else:
                date_match = re.search(r'(\d{2}-\d{2}-\d{4})\s+and\s+(\d{2}-\d{2}-\d{4})', user_input)
                if date_match:
                    start_date, end_date = date_match.groups()
                else:
                    return "Time frame not recognised. Please specify"


            if ticker and start_date and end_date:
                if any(command in user_input.lower() for command in commands_sharpe):
                    sharpe_ratio = calculate_sharpe_ratio(ticker, start_date, end_date)
                    return f"The Sharpe ratio for {ticker} from {start_date} to {end_date} is {sharpe_ratio}"
                elif any(command in user_input.lower() for command in commands_volatility):
                    volatility = calculate_volatility(ticker, start_date, end_date)
                    return f"The volatility for {ticker} from {start_date} to {end_date} is {volatility}"
                
        return None        

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return "Oops, something went wrong. Please try again."

client = OpenAI(api_key=OPENAI_API_KEY)

def get_completion(prompt, client_instance, model="gpt-3.5-turbo"):

    messages = [
        {
        "role": "system", 
         "content" : "You are a helpful assistant guiding the user through querying their cryptocurrency wallet. You give concise but helpful answers. If you are using bullet points in your response, limit them to three."
         }
        ,
        {
            "role": "user", "content": prompt
            }
                ]
    
    response = client_instance.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0,
    )
    return response.choices[0].message.content

def prompt_engineer(user_input, client_instance, model = "gpt-3.5-turbo"):

    # prompt = f"The user said: '{user_input}'. Is the user requesting a specific action (like checking their balance or P&L), or are they asking a general question or making a statement? Please respond with 'action' or 'general'."
    featured_prompts = {
        'Is this a good p&l value?': 'general',
        'What volatility should I be looking for?': 'general',
        'What is the risk of BTC in the last year?': 'action',
        'What is the sharpe ratio of bitcoin within the last year': 'action',
        'What is the volatility of XRP within the last year': 'action',
        'What is the sharpe ratio of bitcoin within the last 6 months': 'action',
        'What is the risk ratio of XRP within the last 6 months': 'action',
        'How does one interpret sharpe ratio?' : 'general',
        'How does on understand and interpret risk/volatility?' : 'general',
        'Which tokens out of those are the least in value?' : 'general',
        'Which tokens out of those are the greatest in value?' : 'general',
        'I want to see the value and balance for all my tokens' : 'action',
        'all my tokens' : 'action'
    }

    prompt = "Consider the following examples to understand user intent:\n"
    for example, category in featured_prompts.items():
        prompt += f"- '{example}' is a {category} query.\n"
    prompt += f"\nThe user said: '{user_input}'. Is the user requesting a specific action or are they asking a general question? Respond with 'action' or 'general'."

    messages = [{"role": "user", "content": prompt}]
    response = client_instance.chat.completions.create(
        model = model,
        messages = messages,
        max_tokens = 500,
        temperature = 0,
    )

    chatbot_decision = response.choices[0].message.content.strip().lower()

    if "action" in chatbot_decision:
        return "yes" 
    else:
        return "no" 
    
# user_input = "I want the p&l of my wallet"
# user_input2 = "Is the p&l good?"
# user_input3 = "What should one do to increase their profit and loss?"
# decision = prompt_engineer(user_input3, client)
# print(decision)

# "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
