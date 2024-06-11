from dateutil import parser
import re

class Utils:
    def format_currency(self, value):
        return "${:,.2f}".format(value)

    def add_percent(self, value):
        return "{:.6f}%".format(value)

    def compact_number_format(self, value):
        billion = 1000000000
        million = 1000000
        if abs(value) >= billion:
            return f"${value / billion:.2f}B"
        elif abs(value) >= million:
            return f"${value / million:.2f}M"
        else:
            return f"${value:,.2f}"
    
    def top_n_by_value(self, data, n):
        return data.sort_values(by='quote', ascending=False).head(n)

    def top_n_by_balance(self, data, n):
        return data.sort_values(by='calculated_balance', ascending=False).head(n)

    def filter_by_token_name(self, data, token_names):
        return data[data['contract_name'].isin(token_names)]

    def extract_ticker(self, user_input):
        match = re.search(r'\b(sharpe ratio|volatility)\s+([A-Z0-9]+)', user_input.upper())
        if match:
            return match.group(2)
        else:
            raise ValueError("Ticker symbol not found in the input.")

class Extracts:
    def parse_dates_from_input(self, input_text):
        parts = input_text.split()
        if len(parts) != 2:
            raise ValueError("Please enter two dates in the format 'dd-mm-yyyy' or 'dd/mm/yyyy'.")

        try:
            start_date = parser.parse(parts[0], dayfirst=True).strftime('%d-%m-%Y')
            end_date = parser.parse(parts[1], dayfirst=True).strftime('%d-%m-%Y')
            return start_date, end_date
        except parser.ParserError as e:
            raise ValueError(str(e))
        
    def extract_ticker(self, user_input, known_tickers):
        user_input = user_input.upper()
        for ticker in known_tickers:
            if ticker in user_input.split():
                return ticker
        raise ValueError("Ticker symbol not found in the input.")