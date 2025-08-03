"""
Exchange Configuration and Utility Functions
Handles exchange setup, API credentials, and common trading utilities.
"""

import ccxt
import requests
import pytz
import datetime
import os
import ast
from colorama import Style, Fore
from typing import Dict, List, Optional, Any

# Configuration Constants
DEFAULT_RENEWAL = False
DEFAULT_DELTA_NEUTRAL = False
DEFAULT_TIMEZONE = 'Europe/Paris'
DEFAULT_PYTHON_COMMAND = 'python3'

# Trading Constants
MIN_ORDER_VALUE_USD = 10.0  # Minimum order value in USD
LARGE_NUMBER = 10e13  # Used for unlimited max values
BTC_USDT_PAIR = 'BTC/USDT'  # Reference pair for fees

# File paths
LOGS_DIR = 'logs'
LOGS_FILE = os.path.join(LOGS_DIR, 'logs.txt')

# Configuration
renewal = True  # Enable renewal functionality for session restarts
delta_neutral = DEFAULT_DELTA_NEUTRAL
timezone = DEFAULT_TIMEZONE
python_command = DEFAULT_PYTHON_COMMAND

# Exchange credentials - users should fill these in
exchanges = {
    'kucoin': {},
    'binance': {},
    'okx': {},
    'poloniex': {},
    # Add more exchanges as needed
    # 'another_exchange_here': {
    #     'apiKey': 'your_api_key_here',
    #     'secret': 'your_secret_here',
    # },
}

# Telegram configuration
telegram_sending = False
apiToken = 'your_telegram_bot_token_here'
chatID = 'your_telegram_chat_id_here'

# Trading criteria
criteria_pct = 0  # Minimum percentage difference
criteria_usd = 0  # Minimum USD profit

# Timeout settings
first_orders_fill_timeout = 0  # Will be set to 3600 if 0

# Demo settings
demo_fake_delay = False
demo_fake_delay_ms = 500

# Utility Functions
def calculate_average(values: List[float]) -> float:
    """Calculate the average of a list of values."""
    if not values:
        return 0.0
    return sum(values) / len(values)

def send_to_telegram(message: str) -> None:
    """Send a message to Telegram."""
    if not telegram_sending:
        return
    
    # Clean up formatting characters for Telegram
    clean_message = message.replace("[2m", "").replace("[0m", "").replace("[32m", "").replace("[31m", "")
    
    api_url = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    
    try:
        response = requests.post(
            api_url, 
            json={'chat_id': chatID, 'text': clean_message},
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

def append_list_to_file(filename: str, new_element: Any) -> None:
    """Append an element to a list stored in a file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data_list = ast.literal_eval(file.read())
        else:
            data_list = []
    except (FileNotFoundError, ValueError, SyntaxError):
        data_list = []

    data_list.append(new_element)

    try:
        with open(filename, 'w') as file:
            file.write(str(data_list))
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def append_new_line(file_name: str, text_to_append: str) -> None:
    """Append a new line to a text file, creating directories if necessary."""
    try:
        # Create directory if it doesn't exist
        dir_name = os.path.dirname(file_name)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Append to file
        with open(file_name, 'a+') as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write('\n')
            file_object.write(text_to_append)
    except IOError as e:
        print(f"Error writing to log file {file_name}: {e}")

def printerror(**kwargs) -> None:
    """Print and log error messages with consistent formatting."""
    message = kwargs.get('m', 'Unknown error occurred')
    name_of_data = kwargs.get('name_of_data')
    data = kwargs.get('data')
    
    # Print to console
    print(f"{get_time()}{Fore.RED}{Style.BRIGHT}Error: {message}{Style.RESET_ALL}")
    
    # Log to file
    log_message = f"{get_time_blank()} ERROR: {message}"
    if name_of_data and data:
        log_message += f" | {name_of_data}: {data}"
    
    append_new_line(LOGS_FILE, log_message)

def get_balance(exchange_name: str, pair: str) -> float:
    """Get the free balance for a specific cryptocurrency on an exchange."""
    try:
        # Extract base currency from pair
        base_currency = pair.split('/')[0] if '/' in pair else pair.replace('/USDT', '')
        
        balance_info = ex[exchange_name].fetch_balance()
        return float(balance_info[base_currency]['free'])
    except (KeyError, ValueError, TypeError):
        return 0.0
    except Exception as e:
        printerror(m=f"Error fetching balance from {exchange_name}: {e}")
        return 0.0

def get_precision_min(pair: str, exchange_name: str) -> Optional[float]:
    """Get the minimum price precision for a trading pair on an exchange."""
    try:
        pair_info = ex[exchange_name].load_markets(pair)
        return pair_info[pair]['limits']['price']['min']
    except Exception as e:
        printerror(m=f"Error getting price precision for {pair} on {exchange_name}: {e}")
        return None

def get_time() -> str:
    """Get formatted timestamp with styling for console output."""
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    timestamp = now.strftime("[%d/%m/%Y %H:%M:%S]")
    return f"{Style.DIM}{timestamp}{Style.RESET_ALL} "

def get_time_blank() -> str:
    """Get formatted timestamp without styling for log files."""
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return now.strftime("[%d/%m/%Y %H:%M:%S]")

def get_balance_usdt(exchange_list: List[str]) -> float:
    """Get total USDT balance across multiple exchanges."""
    total_balance = 0.0
    
    for exchange_name in exchange_list:
        try:
            balances = ex[exchange_name].fetchBalance()
            total_balance += float(balances['USDT']['free'])
        except Exception as e:
            printerror(m=f"Error fetching USDT balance from {exchange_name}: {e}")
    
    return total_balance

def cancel_all_orders(exchange_name: str, pair: str) -> bool:
    """Cancel all open orders for a pair on an exchange."""
    try:
        if not ex[exchange_name].has['cancelAllOrders']:
            return False
        
        open_orders = ex[exchange_name].fetchOpenOrders(pair)
        if not open_orders:
            return True
        
        ex[exchange_name].cancelAllOrders(pair)
        print(f"{get_time()}Successfully canceled all orders on {exchange_name}.")
        append_new_line(LOGS_FILE, f"{get_time_blank()} INFO: Successfully canceled all orders on {exchange_name}.")
        return True
    except Exception as e:
        printerror(m=f"Error canceling orders on {exchange_name}: {e}")
        return False

def emergency_convert_list(pair_to_sell: str, exchange_list: List[str]) -> None:
    """Emergency function to sell all cryptocurrency back to base currency."""
    for exchange_name in exchange_list:
        try:
            # Cancel any open orders first
            cancel_all_orders(exchange_name, pair_to_sell)
            
            # Get current balance
            balance = get_balance(exchange_name, pair_to_sell)
            if balance <= 0:
                print(f"{get_time()}No {pair_to_sell.split('/')[0]} balance on {exchange_name}.")
                continue
            
            # Get market info and current price
            markets = ex[exchange_name].load_markets()
            ticker = ex[exchange_name].fetch_ticker(pair_to_sell)
            current_price = float(ticker['last'])
            
            # Get trading limits
            pair_limits = markets[pair_to_sell]['limits']
            min_cost = pair_limits['cost']['min'] or 0
            min_amount = pair_limits['amount']['min'] or 0
            max_cost = pair_limits['cost']['max'] or LARGE_NUMBER
            max_amount = pair_limits['amount']['max'] or LARGE_NUMBER
            
            # Check if balance meets minimum requirements
            order_value = balance * current_price
            
            if (balance >= min_amount and order_value >= min_cost and 
                balance <= max_amount and order_value <= max_cost and
                order_value >= MIN_ORDER_VALUE_USD):
                
                # Execute market sell order
                ex[exchange_name].createMarketSellOrder(pair_to_sell, balance)
                
                base_currency = pair_to_sell.split('/')[0]
                print(f"{get_time()}Successfully sold {balance:.6f} {base_currency} on {exchange_name}.")
                append_new_line(LOGS_FILE, 
                    f"{get_time_blank()} INFO: Successfully sold {balance:.6f} {base_currency} on {exchange_name}."
                )
            else:
                print(f"{get_time()}Insufficient balance or order below minimum on {exchange_name}.")
                append_new_line(LOGS_FILE, 
                    f"{get_time_blank()} INFO: Insufficient balance on {exchange_name}."
                )
                
        except Exception as e:
            printerror(m=f"Error during emergency conversion on {exchange_name}: {e}")

def printandtelegram(message: str) -> None:
    """Print message to console and send to Telegram."""
    print(message)
    send_to_telegram(message)

# Initialize exchange instances
try:
    ex = {name: getattr(ccxt, name)(config) for name, config in exchanges.items()}
except Exception as e:
    print(f"Error initializing exchanges: {e}")
    ex = {}

# Legacy compatibility (for existing code that uses old function name)
moy = calculate_average
append_list_file = append_list_to_file
