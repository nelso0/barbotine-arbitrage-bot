#!/usr/bin/env python3
"""
Barbotine Arbitrage Bot - Unified Entry Point
A cryptocurrency arbitrage trading bot for both simulation and live trading.

⚠️  WARNING: This bot can trade with real money when using real mode.
⚠️  Always test thoroughly in fake-money mode before using real funds.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path
from colorama import Style, init, Fore
from typing import List, Optional

# Initialize colorama for cross-platform colored output
init()

# Import configuration after ensuring proper encoding
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

try:
    from exchange_config import (
        ex, python_command, renewal, printerror, get_time, 
        emergency_convert_list, append_new_line
    )
except ImportError as e:
    print(f"Error importing exchange_config: {e}")
    sys.exit(1)

# Constants
DEFAULT_RENEWAL_MINUTES = 525600  # 1 year in minutes
SUPPORTED_MODES = ['fake-money', 'real']
BALANCE_FILE = 'real_balance.txt'  # For fake money mode
USABLE_BALANCE_FILE = 'usable_balance.txt'  # For real money mode
TOTAL_BALANCE_FILE = 'total_balance.txt'  # For real money mode

def display_banner():
    """Display the application banner."""
    banner = '''
                                                                                                                     
                                                                                                                     
VMA""YMM      `7MM"""Yp,      db      `7MM"""Mq.  `7MM"""Yp,   .g8""8q.  MMP""MM""YMM `7MMF'`7MN.   `7MF'`7MM"""YMM  
 VMA  `7        MM    Yb     ;MM:       MM   `MM.   MM    Yb .dP'    `YM.P'   MM   `7   MM    MMN.    M    MM    `7  
  VMA           MM    dP    ,V^MM.      MM   ,M9    MM    dP dM'      `MM     MM        MM    M YMb   M    MM   d    
   XV           MM"""bg.   ,M  `MM      MMmmdM9     MM"""bg. MM        MM     MM        MM    M  `MN. M    MMmmMM    
  AV    ,       MM    `Y   AbmmmqMA     MM  YM.     MM    `Y MM.      ,MP     MM        MM    M   `MM.M    MM   Y  , 
 AV    ,M       MM    ,9  A'     VML    MM   `Mb.   MM    ,9 `Mb.    ,dP'     MM        MM    M     YMM    MM     ,M 
AMMMMMMMF     .JMMmmmd9 .AMA.   .AMMA..JMML. .JMM..JMMmmmd9    `"bmmd"'     .JMML.    .JMML..JML.    YM  .JMMmmmmMMM 
                                                                                                                     
                                                                                                                     '''
    print(banner)
    
    # Detect if we're in fake money or real money mode based on available files
    is_real_money_mode = os.path.exists('bot.py')
    
    if is_real_money_mode:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}FULL VERSION{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.BLUE}{Style.BRIGHT}DEMO VERSION{Style.RESET_ALL}\n")
    
    print("Website: https://barbotine.xyz\n")

def validate_exchanges(exchange_list: str, mode: str) -> List[str]:
    """Validate that all specified exchanges are supported."""
    exchanges = [e.strip() for e in exchange_list.split(',')]
    
    for exchange in exchanges:
        if exchange not in ex and mode != 'fake-money':
            raise ValueError(f"Unsupported exchange: {exchange}")
    
    return exchanges

def calculate_real_balance(pair: str, exchanges: List[str]) -> float:
    """Calculate total real balance across exchanges."""
    quote_currency = pair.split('/')[1]
    total_balance = 0.0
    
    for exchange_name in exchanges:
        try:
            balance = ex[exchange_name].fetchBalance()
            total_balance += float(balance[quote_currency]['total'])
        except Exception as e:
            printerror(m=f"Error fetching balance from {exchange_name}: {e}")
            raise
    
    return total_balance

def save_balance_files(balance: float, mode: str, total_balance: Optional[float] = None) -> None:
    """Save balance to appropriate files based on mode."""
    try:
        if mode == 'fake-money':
            with open(BALANCE_FILE, "w") as f:
                f.write(str(balance))
        else:
            # Real money mode
            with open(USABLE_BALANCE_FILE, "w") as f:
                f.write(str(balance))
            if total_balance is not None:
                with open(TOTAL_BALANCE_FILE, "w") as f:
                    f.write(str(total_balance))
    except IOError as e:
        printerror(m=f"Error saving balance files: {e}")
        raise

def load_balance(mode: str) -> float:
    """Load balance from appropriate file based on mode."""
    try:
        file_to_read = BALANCE_FILE if mode == 'fake-money' else USABLE_BALANCE_FILE
        with open(file_to_read, "r") as f:
            return float(f.read().strip())
    except (IOError, ValueError) as e:
        printerror(m=f"Error loading balance: {e}")
        return 0.0

def run_bot(mode: str, pair: str, balance: str, renewal_time: str, exchange_list: str) -> int:
    """Run the appropriate bot based on mode."""
    if mode == "fake-money":
        bot_file = "bot-fake-money.py"
    elif mode == "real":
        bot_file = "bot.py"
        # Check if real money bot exists
        if not os.path.exists(bot_file):
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  Real money bot not found!{Style.RESET_ALL}")
            print("The real money trading files (bot.py) are not available in this version.")
            print("Please visit https://barbotine.xyz for more information about accessing the full version.")
            return 1
    else:
        printerror(m=f"Invalid mode: {mode}")
        return 1
    
    if not os.path.exists(bot_file):
        printerror(m=f'Bot file "{bot_file}" not found in current directory.')
        return 1
    
    try:
        process = subprocess.run([
            python_command, bot_file, pair, balance, 
            renewal_time, pair, exchange_list
        ])
        return process.returncode
    except Exception as e:
        printerror(m=f"Error running bot: {e}")
        return 1

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Barbotine Arbitrage Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py fake-money 1000 BTC/USDT binance,kucoin
  python3 main.py real 500 ETH/USDT binance,kucoin,okx
  python3 main.py fake-money 1000 BTC/USDT binance,kucoin 60  # with 60min renewal
        """
    )
    
    parser.add_argument(
        "mode", 
        choices=SUPPORTED_MODES,
        help="Trading mode (fake-money for simulation, real for live trading)"
    )
    
    parser.add_argument(
        "balance",
        type=float,
        help="Balance to use for trading"
    )
    
    parser.add_argument(
        "pair",
        help="Trading pair (e.g., BTC/USDT)"
    )
    
    parser.add_argument(
        "exchanges",
        help="Comma-separated list of exchanges (e.g., binance,kucoin)"
    )
    
    parser.add_argument(
        "renewal_time",
        type=int,
        nargs='?',  # Make it optional
        default=DEFAULT_RENEWAL_MINUTES,
        help="Optional: Renewal period in minutes (if not specified, runs once)"
    )
    
    return parser.parse_args()

def interactive_input() -> dict:
    """Get parameters through interactive input."""
    inputs = {}
    
    try:
        inputs['mode'] = input("Mode (fake-money or real) >>> ").strip()
        if inputs['mode'] not in SUPPORTED_MODES:
            raise ValueError(f"Invalid mode. Must be one of: {SUPPORTED_MODES}")
        
        # Check for real money mode availability
        if inputs['mode'] == 'real' and not os.path.exists('bot.py'):
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  Real money mode not available!{Style.RESET_ALL}")
            print("The real money trading files are not available in this version.")
            print("Please visit https://barbotine.xyz for more information about accessing the full version.")
            sys.exit(0)
        
        # Show warning for real money mode
        if inputs['mode'] == 'real':
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  WARNING: You selected REAL MONEY mode!{Style.RESET_ALL}")
            print("This will trade with actual funds. Make sure you:")
            print("1. Have tested thoroughly in fake-money mode")
            print("2. Have proper API credentials configured")
            print("3. Understand the risks involved")
            confirm = input("\nType 'I UNDERSTAND' to continue: ").strip()
            if confirm != 'I UNDERSTAND':
                print("Aborting for safety.")
                sys.exit(0)
        
        # Ask if user wants renewal
        if renewal:
            enable_renewal = input("Enable session renewal? (y/N) >>> ").strip().lower()
            if enable_renewal in ['y', 'yes']:
                inputs['renewal_time'] = int(input("Renewal period (in minutes) >>> "))
            else:
                inputs['renewal_time'] = DEFAULT_RENEWAL_MINUTES
        else:
            inputs['renewal_time'] = DEFAULT_RENEWAL_MINUTES
        
        inputs['balance'] = float(input("Balance to use >>> "))
        inputs['pair'] = input("Trading pair (e.g., BTC/USDT) >>> ").strip().upper()
        inputs['exchanges'] = input("Exchanges (comma-separated) >>> ").strip()
        
        return inputs
    except (ValueError, KeyboardInterrupt) as e:
        printerror(m=f"Invalid input: {e}")
        sys.exit(1)

def clear_screen():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def handle_emergency_exit(mode: str, pair: str, exchanges: List[str]) -> None:
    """Handle emergency exit procedures for real money mode."""
    if mode != 'real':
        return
    
    print("\n\n")
    clear_screen()
    
    answered = False
    while not answered:
        try:
            response = input(f"{get_time()}CTRL+C was pressed. Do you want to sell all crypto back? (y)es / (n)o\n\nInput: ")
            append_new_line('logs/logs.txt', f"{get_time()} INFO: CTRL+C was pressed.")
            
            if response.lower() in ['y', 'yes']:
                answered = True
                print(f"{get_time()}Initiating emergency liquidation...")
                emergency_convert_list(pair, exchanges)
                print(f"{get_time()}Emergency liquidation completed.")
                sys.exit(1)
            elif response.lower() in ['n', 'no']:
                answered = True
                print(f"{get_time()}Exiting without liquidation.")
                sys.exit(1)
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                answered = False
        except KeyboardInterrupt:
            print("\nForced exit.")
            sys.exit(1)

def main():
    """Main application entry point."""
    display_banner()
    
    try:
        # Get parameters from command line or interactive input
        if len(sys.argv) > 1:
            args = parse_arguments()
            mode = args.mode
            pair = args.pair
            balance = str(args.balance)
            exchanges_str = args.exchanges
            renewal_time = str(args.renewal_time)
        else:
            inputs = interactive_input()
            mode = inputs['mode']
            pair = inputs['pair']
            balance = str(inputs['balance'])
            exchanges_str = inputs['exchanges']
            renewal_time = str(inputs['renewal_time'])
        
        # Validate exchanges
        exchanges = validate_exchanges(exchanges_str, mode)
        
        # Calculate and save initial balance
        if mode != 'fake-money':
            print(f"{get_time()}Calculating real balances across exchanges...")
            total_balance = calculate_real_balance(pair, exchanges)
            save_balance_files(float(balance), mode, total_balance)
            print(f"{get_time()}Usable balance: {balance} {pair.split('/')[1]}")
            print(f"{get_time()}Total balance across exchanges: {total_balance} {pair.split('/')[1]}")
        else:
            save_balance_files(float(balance), mode)
        
        # Main bot execution loop with renewal support
        session_count = 0
        
        while True:
            session_count += 1
            current_balance = str(load_balance(mode))
            
            print(f"{get_time()}Starting session #{session_count}")
            
            return_code = run_bot(mode, pair, current_balance, renewal_time, exchanges_str)
            
            if return_code != 0:
                printerror(m="Bot execution failed")
                sys.exit(1)
            
            # Check if renewal is enabled and this isn't a one-time run
            if not renewal or int(renewal_time) >= DEFAULT_RENEWAL_MINUTES:
                print(f"{get_time()}Session completed. Exiting (no renewal).")
                break
            
            # If renewal is enabled, continue the loop for next session
            print(f"{get_time()}Session #{session_count} completed. Restarting in 5 seconds...")
            import time
            time.sleep(5)
            
    except KeyboardInterrupt:
        if 'mode' in locals() and 'exchanges' in locals() and 'pair' in locals():
            handle_emergency_exit(mode, pair, exchanges)
        else:
            print("\nExiting...")
            sys.exit(1)
    except Exception as e:
        printerror(m=f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
