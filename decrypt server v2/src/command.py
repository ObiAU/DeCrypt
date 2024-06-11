from tokenomics import Tokenomics
from utility import Utils
from models import Model
from datetime import datetime, timedelta
import re

class Commander(Tokenomics, Utils):
    def __init__(self) -> None:
        super().__init__()

    def check_for_command(self, user_input, wallet_address, is_web=False, extra_data=None):
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

            response = self.get_token_balances(wallet_address)

            # unique_tickers = response['contract_ticker_symbol'].unique()
            # known_tickers.extend(ticker for ticker in unique_tickers if ticker not in known_tickers)

            if response.empty:
                return "Error: Unable to retrieve data from API."

            if "top" in user_input.lower():  
                match = re.search(r"top (\d+)", user_input.lower())
                if match:
                    n = int(match.group(1))
                    
                    if "by value" in user_input.lower():
                        filtered_data = self.top_n_by_value(response, n)
                        return self.formatted_token_balances(filtered_data)
                    
                    elif "by balance" in user_input.lower():
                        filtered_data = self.top_n_by_balance(response, n)
                        return self.formatted_token_balances(filtered_data)
                else:
                    return "Error: Could not find a number in your query."

            elif "token name" in user_input.lower():
                names = user_input.replace("token name", "").split(",")
                names = [name.strip() for name in names]
                filtered_data = self.filter_by_token_name(response, names)
                return self.formatted_token_balances(filtered_data)

            elif "limit" in user_input.lower():
                limit = int(user_input.split(" ")[1])
                return self.formatted_token_balances(response.head(limit))
            
            # token balance
            elif any(command in user_input.lower() for command in commands_balance):
                return self.formatted_token_balances(response)
            
            # p&l
            # elif any(command in user_input.lower() for command in currency_conversions):
            #     ans = None
            #     for curr in currency_conversions:
            #         ans = curr.lower() 
            #         return f"The profit and loss in {ans} is {self.calculate_profit_and_loss(response, ans)}"
                
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
                        pnl_result = self.calculate_profit_and_loss(response, selected_currency, type=pnl_type, token=selected_token)
                        return f"Sure, the profit and loss in your wallet {selected_currency} for {selected_token} over the last 24 hours is {pnl_result}"
                    else:
                        pnl_result = self.calculate_profit_and_loss(response, selected_currency, type=pnl_type, token=None)
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
                    return self.price_change_analysis(response, token= ptoken)
                else:
                    return self.price_change_analysis(response)

            # holdings calculations
            elif any(command in user_input.lower() for command in commands_holdings):
                if 'current' in user_input.lower():
                    return self.calculate_holdings(response, time=None)
                elif 'difference' in user_input.lower() or 'change' in user_input.lower() or '24 hours' in user_input.lower() or '24h' in user_input.lower():
                    return self.difference_in_holdings(response)
                else:
                    return self.calculate_holdings(response, time=1)
                
                
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
                        sharpe_ratio = self.calculate_sharpe_ratio(ticker, start_date, end_date)
                        return f"The Sharpe ratio for {ticker} from {start_date} to {end_date} is {sharpe_ratio}"
                    elif any(command in user_input.lower() for command in commands_volatility):
                        volatility = self.calculate_volatility(ticker, start_date, end_date)
                        return f"The volatility for {ticker} from {start_date} to {end_date} is {volatility}"
                    
            return None        

        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return "Oops, something went wrong. Please try again."