#!/usr/bin/env python3
"""
Barbotine Arbitrage Bot - Fake Money Mode
Simulates arbitrage trading with fake money for testing and demonstration.
"""

import asyncio
import time
import sys
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass

import ccxt.pro
import ccxt
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

# Import configuration
from exchange_config import (
    ex, python_command, first_orders_fill_timeout, demo_fake_delay, 
    demo_fake_delay_ms, criteria_pct, criteria_usd, printerror, 
    get_time, get_time_blank, append_new_line, append_list_to_file,
    printandtelegram, calculate_average, send_to_telegram, get_balance,
    emergency_convert_list
)

# Constants
REQUIRED_ARGS = 6
MIN_ORDER_VALUE_USD = 10.0
DEFAULT_TIMEOUT_SECONDS = 3600
CONSOLE_CLEAR_LINES = 2

@dataclass
class TradingState:
    """Holds the current trading state."""
    bid_prices: Dict[str, float]
    ask_prices: Dict[str, float]
    total_profit_usd: float
    previous_ask_price: float
    previous_bid_price: float
    opportunity_count: int
    iteration_count: int
    stop_requested: bool
    
    def __init__(self):
        self.bid_prices = {}
        self.ask_prices = {}
        self.total_profit_usd = 0.0
        self.previous_ask_price = 0.0
        self.previous_bid_price = 0.0
        self.opportunity_count = 0
        self.iteration_count = 0
        self.stop_requested = False

@dataclass
class TradingConfig:
    """Configuration for the trading session."""
    pair: str
    base_currency: str
    quote_currency: str
    total_investment_usd: float
    timeout_minutes: int
    session_title: str
    exchange_names: List[str]
    exchange_instances: List[object]
    
def validate_arguments() -> None:
    """Validate command line arguments."""
    if len(sys.argv) != REQUIRED_ARGS:
        print(f"\nIncorrect usage. Expected format:")
        print(f"{python_command} bot-fake-money.py [pair] [total_usdt_investment] [timeout_minutes] [session_title] [exchange_list]")
        print(f"\nReceived arguments: {sys.argv}")
        sys.exit(1)

def setup_exchanges(exchange_list_str: str) -> List[str]:
    """Setup and validate exchange instances."""
    exchange_names = exchange_list_str.split(',')
    
    # Initialize missing exchanges
    for exchange_name in exchange_names:
        if exchange_name not in ex:
            try:
                ex[exchange_name] = getattr(ccxt, exchange_name)()
            except AttributeError:
                printerror(m=f"Unsupported exchange: {exchange_name}")
                sys.exit(1)
    
    return exchange_names

def calculate_fees(exchange_names: List[str]) -> Dict[str, Dict[str, float]]:
    """Calculate trading fees for each exchange."""
    fees = {}
    
    for exchange_name in exchange_names:
        try:
            markets = ex[exchange_name].load_markets()
            btc_usdt_info = markets.get('BTC/USDT', {})
            
            # Extract fee information
            fee_side = btc_usdt_info.get('feeSide')
            taker_fee = btc_usdt_info.get('taker', 0)
            
            if fee_side:
                fees[exchange_name] = {
                    'base': taker_fee if fee_side == 'base' else 0,
                    'quote': 0 if fee_side == 'base' else taker_fee
                }
            else:
                fees[exchange_name] = {'base': 0, 'quote': taker_fee}
                
        except Exception as e:
            printerror(m=f"Error calculating fees for {exchange_name}: {e}")
            fees[exchange_name] = {'base': 0.001, 'quote': 0.001}  # Default 0.1%
    
    return fees

def listen_for_manual_exit(state: TradingState) -> None:
    """Listen for user input to request manual exit."""
    try:
        input("")  # Wait for any input
        state.stop_requested = True
    except:
        pass

async def fetch_orderbook_safe(exchange_instance, pair: str) -> Optional[dict]:
    """Safely fetch orderbook with error handling and retry logic."""
    try:
        orderbook = await exchange_instance.watch_order_book(pair)
        return orderbook
    except Exception as e:
        printerror(m=f"Error fetching orderbook from {exchange_instance.id}: {e}")
        
        # Clear console lines
        for _ in range(CONSOLE_CLEAR_LINES):
            sys.stdout.write("\033[F\033[K")
        
        # Try to recreate the exchange instance
        try:
            exchange_id = exchange_instance.id
            await exchange_instance.close()
            new_instance = getattr(ccxt.pro, exchange_id)({'enableRateLimit': True})
            orderbook = await new_instance.watch_order_book(pair)
            return orderbook
        except Exception as retry_error:
            printerror(m=f"Failed to retry orderbook fetch: {retry_error}")
            return None

def clear_console_lines(count: int) -> None:
    """Clear specified number of lines from console."""
    for _ in range(count):
        sys.stdout.write("\033[F\033[K")

def calculate_theoretical_balances(
    usd_balances: Dict[str, float],
    crypto_balances: Dict[str, float],
    min_ask_exchange: str,
    max_bid_exchange: str,
    min_ask_price: float,
    max_bid_price: float,
    crypto_per_transaction: float,
    fees: Dict[str, Dict[str, float]]
) -> tuple:
    """Calculate theoretical balances after a trade."""
    
    # Calculate cost of buying on min_ask exchange
    buy_cost = (crypto_per_transaction / (1 - fees[min_ask_exchange]['quote'])) * \
               min_ask_price * (1 + fees[min_ask_exchange]['base'])
    
    # Calculate proceeds from selling on max_bid exchange  
    sell_proceeds = (crypto_per_transaction / (1 + fees[max_bid_exchange]['base'])) * \
                   max_bid_price * (1 - fees[max_bid_exchange]['quote'])
    
    theoretical_min_ask_usd = usd_balances[min_ask_exchange] - buy_cost
    theoretical_max_bid_usd = usd_balances[max_bid_exchange] + sell_proceeds
    
    return theoretical_min_ask_usd, theoretical_max_bid_usd

def format_exchange_balances(
    crypto_balances: Dict[str, float], 
    usd_balances: Dict[str, float],
    base_currency: str,
    quote_currency: str
) -> str:
    """Format exchange balances for display."""
    balance_lines = []
    for exchange_name in crypto_balances:
        crypto_amount = round(crypto_balances[exchange_name], 6)
        usd_amount = round(usd_balances[exchange_name], 2)
        balance_lines.append(f"➝ {exchange_name}: {crypto_amount} {base_currency} / {usd_amount} {quote_currency}")
    
    return "\n".join(balance_lines)

def simulate_order_delay(min_ask_exchange: str, max_bid_exchange: str, pair: str) -> tuple:
    """Simulate network delay and return updated prices."""
    if not demo_fake_delay:
        return None, None
    
    asyncio.run(asyncio.sleep(demo_fake_delay_ms / 1000))
    
    try:
        min_ask_ob = asyncio.run(fetch_orderbook_safe(getattr(ccxt, min_ask_exchange)(), pair))
        max_bid_ob = asyncio.run(fetch_orderbook_safe(getattr(ccxt, max_bid_exchange)(), pair))
        
        if min_ask_ob and max_bid_ob:
            return min_ask_ob['asks'][0][0], max_bid_ob['bids'][0][0]
    except Exception as e:
        printerror(m=f"Error in delay simulation: {e}")
    
    return None, None

def execute_simulated_trades(
    min_ask_exchange: str,
    max_bid_exchange: str, 
    min_ask_price: float,
    max_bid_price: float,
    crypto_per_transaction: float,
    profit_usd: float,
    crypto_balances: Dict[str, float],
    usd_balances: Dict[str, float],
    fees: Dict[str, Dict[str, float]],
    base_currency: str
) -> None:
    """Execute simulated arbitrage trades and update balances."""
    
    # Log the trades
    printandtelegram(f"{get_time()}Sell market order filled on {max_bid_exchange} "
                    f"for {crypto_per_transaction:.6f} {base_currency} at {max_bid_price}")
    printandtelegram(f"{get_time()}Buy market order filled on {min_ask_exchange} "
                    f"for {crypto_per_transaction:.6f} {base_currency} at {min_ask_price}")
    
    # Record the profit
    append_list_to_file('all_opportunities_profits.txt', profit_usd)
    
    # Update balances
    # Buy on min_ask exchange
    crypto_balances[min_ask_exchange] += crypto_per_transaction
    buy_cost = (crypto_per_transaction / (1 - fees[min_ask_exchange]['quote'])) * \
               min_ask_price * (1 + fees[min_ask_exchange]['base'])
    usd_balances[min_ask_exchange] -= buy_cost
    
    # Sell on max_bid exchange
    crypto_balances[max_bid_exchange] -= crypto_per_transaction
    sell_proceeds = (crypto_per_transaction / (1 + fees[max_bid_exchange]['base'])) * \
                   max_bid_price * (1 - fees[max_bid_exchange]['quote'])
    usd_balances[max_bid_exchange] += sell_proceeds

async def monitor_arbitrage_opportunities(
    exchange_instance,
    config: TradingConfig,
    state: TradingState,
    crypto_balances: Dict[str, float],
    usd_balances: Dict[str, float],
    fees: Dict[str, Dict[str, float]],
    crypto_per_transaction: float,
    session_start_time: float,
    timeout_timestamp: float
) -> None:
    """Monitor for arbitrage opportunities on a single exchange."""
    
    while time.time() <= timeout_timestamp:
        if state.stop_requested:
            clear_console_lines(CONSOLE_CLEAR_LINES)
            print(f"{get_time()}Manual rebalance requested. Breaking.")
            append_new_line('logs/logs.txt', f"{get_time_blank()} INFO: Manual rebalance requested.")
            await exchange_instance.close()
            break
        
        # Fetch orderbook
        orderbook = await fetch_orderbook_safe(exchange_instance, config.pair)
        if not orderbook:
            continue
        
        # Update price data
        state.bid_prices[exchange_instance.id] = orderbook["bids"][0][0]
        state.ask_prices[exchange_instance.id] = orderbook["asks"][0][0]
        
        # Find best arbitrage opportunity
        min_ask_exchange = min(state.ask_prices, key=state.ask_prices.get)
        max_bid_exchange = max(state.bid_prices, key=state.bid_prices.get)
        
        # Adjust for available balances
        for exchange_name in config.exchange_names:
            if crypto_balances[exchange_name] < crypto_per_transaction:
                min_ask_exchange = exchange_name
            if usd_balances[exchange_name] <= 0:
                max_bid_exchange = exchange_name
        
        min_ask_price = state.ask_prices[min_ask_exchange]
        max_bid_price = state.bid_prices[max_bid_exchange]
        
        # Calculate theoretical profit
        theoretical_min_ask_usd, theoretical_max_bid_usd = calculate_theoretical_balances(
            usd_balances, crypto_balances, min_ask_exchange, max_bid_exchange,
            min_ask_price, max_bid_price, crypto_per_transaction, fees
        )
        
        profit_usd = (theoretical_min_ask_usd + theoretical_max_bid_usd) - \
                    (usd_balances[max_bid_exchange] + usd_balances[min_ask_exchange])
        
        # Check if opportunity meets criteria
        price_diff_pct = abs(min_ask_price - max_bid_price) / ((max_bid_price + min_ask_price) / 2) * 100
        
        is_profitable = (
            max_bid_exchange != min_ask_exchange and
            profit_usd > float(criteria_usd) and
            price_diff_pct >= criteria_pct and
            state.previous_ask_price != min_ask_price and
            state.previous_bid_price != max_bid_price
        )
        
        if is_profitable:
            state.opportunity_count += 1
            
            # Calculate fees for display
            fees_crypto = crypto_per_transaction * (fees[min_ask_exchange]['quote'] + fees[max_bid_exchange]['base'])
            fees_usd = (crypto_per_transaction * max_bid_price * fees[max_bid_exchange]['quote'] + 
                       crypto_per_transaction * min_ask_price * fees[min_ask_exchange]['base'])
            
            # Clear console and display opportunity
            clear_console_lines(1)
            print("-----------------------------------------------------")
            
            exchange_balances = format_exchange_balances(
                crypto_balances, usd_balances, config.base_currency, config.quote_currency
            )
            
            elapsed_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - session_start_time))
            
            print(f"{Style.RESET_ALL}Opportunity #{state.opportunity_count} detected! "
                  f"({min_ask_exchange} {min_ask_price} -> {max_bid_price} {max_bid_exchange})\n")
            print(f"Expected profit: {Fore.GREEN}+{round(profit_usd, 4)} {config.quote_currency}{Style.RESET_ALL}")
            print(f"Session total profit: {Fore.GREEN}+{round(state.total_profit_usd, 4)} {config.quote_currency}{Style.RESET_ALL}")
            print(f"Fees paid: {Fore.RED}-{round(fees_usd, 4)} {config.quote_currency} -{round(fees_crypto, 4)} {config.base_currency}")
            print(f"{Style.DIM}{exchange_balances}")
            print(f"Time elapsed: {elapsed_time}")
            print("-----------------------------------------------------\n")
            
            # Send Telegram notification
            telegram_msg = (f"[{config.session_title} Trade #{state.opportunity_count}]\n\n"
                          f"Opportunity detected!\n"
                          f"Expected profit: {round(profit_usd, 4)} {config.quote_currency}\n"
                          f"{min_ask_exchange} {min_ask_price} -> {max_bid_price} {max_bid_exchange}\n"
                          f"Time elapsed: {elapsed_time}\n"
                          f"Session total profit: {round(state.total_profit_usd, 4)} {config.quote_currency}\n"
                          f"Fees: {round(fees_usd, 4)} {config.quote_currency} {round(fees_crypto, 4)} {config.base_currency}\n\n"
                          f"--------BALANCES--------\n{exchange_balances}")
            send_to_telegram(telegram_msg)
            
            # Simulate order delay if enabled
            if demo_fake_delay:
                timestamp = time.time()
                delayed_ask, delayed_bid = simulate_order_delay(min_ask_exchange, max_bid_exchange, config.pair)
                if delayed_ask and delayed_bid:
                    min_ask_price, max_bid_price = delayed_ask, delayed_bid
                    delay_ms = int(round(1000 * (time.time() - timestamp), 0))
                    printandtelegram(f"{get_time()}Calculated P&L with {delay_ms}ms simulated delay")
            
            # Execute simulated trades
            execute_simulated_trades(
                min_ask_exchange, max_bid_exchange, min_ask_price, max_bid_price,
                crypto_per_transaction, profit_usd, crypto_balances, usd_balances,
                fees, config.base_currency
            )
            
            state.total_profit_usd += profit_usd
            state.previous_ask_price = min_ask_price
            state.previous_bid_price = max_bid_price
            
            # Recalculate crypto per transaction
            total_crypto = sum(crypto_balances.values())
            crypto_per_transaction = total_crypto / len(config.exchange_names)
        
        else:
            # Display current best opportunity
            clear_console_lines(1)
            
            color = Fore.GREEN if profit_usd > 0 else Fore.RED if profit_usd < 0 else Fore.WHITE
            
            print(f"{get_time()}Best opportunity: {color}{round(profit_usd, 4)} {config.quote_currency}{Style.RESET_ALL} "
                  f"(with fees) buy: {min_ask_exchange} at {min_ask_price} sell: {max_bid_exchange} at {max_bid_price}")

def simulate_initial_orders(config: TradingConfig, average_price: float, total_crypto: float) -> None:
    """Simulate the initial order placement that would happen in real money mode."""
    printandtelegram(f"{get_time()}Fetching the global average price for {config.pair}...")
    printandtelegram(f"{get_time()}Average {config.pair} price in {config.quote_currency}: {average_price}")
    
    # Simulate placing initial buy orders
    crypto_per_exchange = total_crypto / len(config.exchange_names)
    
    orders_filled = 0
    target_orders = len(config.exchange_names)
    
    # Show order placement simulation
    for i, exchange_name in enumerate(config.exchange_names):
        time.sleep(0.7)  # Simulate network delay
        printandtelegram(f'{get_time()}Buy limit order of {round(crypto_per_exchange, 6)} '
                        f'{config.base_currency} at {average_price} sent to {exchange_name}.')
    
    printandtelegram(f"{get_time()}All orders sent.")
    
    # Simulate order filling process
    while orders_filled != target_orders:
        for exchange_name in config.exchange_names:
            if orders_filled >= target_orders:
                break
            time.sleep(2.1)  # Simulate order fill time
            printandtelegram(f"{get_time()}{exchange_name} order filled.")
            orders_filled += 1

async def run_arbitrage_session(config: TradingConfig) -> None:
    """Run the main arbitrage monitoring session."""
    state = TradingState()
    
    # Setup initial balances
    usd_balances = {exchange: (config.total_investment_usd / 2) / len(config.exchange_names) 
                   for exchange in config.exchange_names}
    
    # Get average price and calculate initial crypto allocation
    all_prices = []
    for exchange_instance in config.exchange_instances:
        try:
            ticker = exchange_instance.fetch_ticker(config.pair)
            all_prices.append(ticker['last'])
        except Exception as e:
            printerror(m=f"Error fetching ticker from {exchange_instance.id}: {e}")
    
    if not all_prices:
        printerror(m="Could not fetch any price data")
        return
    
    average_price = calculate_average(all_prices)
    total_crypto = (config.total_investment_usd / 2) / average_price
    crypto_balances = {exchange: total_crypto / len(config.exchange_names) 
                      for exchange in config.exchange_names}
    
    # Simulate the initial order placement process (like real money mode would do)
    simulate_initial_orders(config, average_price, total_crypto)
    
    time.sleep(1)  # Brief pause before starting main session
    printandtelegram(f"{get_time()}Starting arbitrage monitoring with parameters: {sys.argv}")
    
    # Calculate fees
    fees = calculate_fees(config.exchange_names)
    
    # Initial crypto per transaction
    crypto_per_transaction = total_crypto / len(config.exchange_names)
    
    # Setup session parameters
    session_start_time = time.time()
    timeout_timestamp = time.time() + (config.timeout_minutes * 60)
    
    # Start listener thread for manual exit
    listener_thread = threading.Thread(target=listen_for_manual_exit, args=(state,))
    listener_thread.daemon = True
    listener_thread.start()
    
    # Create exchange monitoring tasks
    exchange_tasks = []
    for exchange_instance in config.exchange_instances:
        pro_exchange = getattr(ccxt.pro, exchange_instance.id)()
        task = monitor_arbitrage_opportunities(
            pro_exchange, config, state, crypto_balances, usd_balances,
            fees, crypto_per_transaction, session_start_time, timeout_timestamp
        )
        exchange_tasks.append(task)
    
    # Run all monitoring tasks
    await asyncio.gather(*exchange_tasks)
    
    # Calculate final balances
    total_final_balance = 0.0
    for exchange_name in config.exchange_names:
        try:
            ticker = ex[exchange_name].fetchTicker(config.pair)
            current_price = ticker['last']
            usd_balances[exchange_name] += crypto_balances[exchange_name] * current_price
            crypto_balances[exchange_name] = 0
            total_final_balance += usd_balances[exchange_name]
        except Exception as e:
            printerror(m=f"Error calculating final balance for {exchange_name}: {e}")
    
    # Update balance file and display results
    try:
        with open('real_balance.txt', 'r+') as balance_file:
            initial_balance = float(balance_file.read())
            balance_file.seek(0)
            balance_file.write(str(total_final_balance))
        
        session_profit = total_final_balance - initial_balance
        printandtelegram(f"{get_time()}Session finished.")
        printandtelegram(f"{get_time()}Total session profit: {session_profit:.4f} {config.quote_currency}")
        
    except Exception as e:
        printerror(m=f"Error updating final balance: {e}")

def main():
    """Main entry point for the fake money bot."""
    # Validate arguments
    validate_arguments()
    
    # Set timeout if not configured
    global first_orders_fill_timeout
    if first_orders_fill_timeout <= 0:
        first_orders_fill_timeout = DEFAULT_TIMEOUT_SECONDS
    
    # Parse arguments
    pair = str(sys.argv[1]).upper()
    total_investment = float(sys.argv[2])
    timeout_minutes = int(sys.argv[3])
    session_title = str(sys.argv[4])
    exchange_list_str = sys.argv[5]
    
    # Setup configuration
    exchange_names = setup_exchanges(exchange_list_str)
    exchange_instances = [ex[name] for name in exchange_names]
    
    config = TradingConfig(
        pair=pair,
        base_currency=pair.split('/')[0],
        quote_currency=pair.split('/')[1],
        total_investment_usd=total_investment,
        timeout_minutes=timeout_minutes,
        session_title=session_title,
        exchange_names=exchange_names,
        exchange_instances=exchange_instances
    )
    
    print()  # Add spacing
    
    # Run the arbitrage session
    asyncio.run(run_arbitrage_session(config))

if __name__ == "__main__":
    main()
