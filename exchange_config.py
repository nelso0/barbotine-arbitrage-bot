import ccxt as ccxt
import requests
import pytz
from colorama import Style,Fore
import datetime

# The bot seems complicated? It's not, just try! (and contact me if you have an error, it's probably a silly one :)

renewal = False
delta_neutral = False
timezone = 'Europe/Paris'
python_command = 'python3'

exchanges = {
    'kucoin':{},
    'binance':{},
    'okx':{},
    'poloniex':{},
    # 'another_exchange_here':{
    #     'apiKey':'here',
    #     'secret':'here',
    # },
}

telegram_sending = False
apiToken = 'here'
chatID = 'here'

criteria_pct = 0
criteria_usd = 0

first_orders_fill_timeout = 0

demo_fake_delay = False
demo_fake_delay_ms = 500

# ------------------------------------ FUNCTIONS (you can ignore) ------------------------------------

def moy(list1):
    moy=0
    for n in list1:
        moy+=n
    return moy/len(list1)
def send_to_telegram(message):
    message = message.replace("[2m","")
    message = message.replace("[0m","")
    message = message.replace("[2m","")
    message = message.replace("[32m","")
    message = message.replace("[31m","")
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        if telegram_sending:
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message}) # put this if you want to send telegram messages.
        else:
            pass
    except Exception as e:
        print(e)
def append_list_file(fichier, nouvel_element):
    import ast
    try:
        with open(fichier, 'r') as file:
            liste = ast.literal_eval(file.read())
    except FileNotFoundError:
        liste = []

    liste.append(nouvel_element)

    with open(fichier, 'w') as file:
        file.write(str(liste))
def append_new_line(file_name, text_to_append):
    import os
    """Appends a new line to a text file, creating directories if necessary.

    Args:
        file_name: The path to the file, including any directories.
        text_to_append: The text to append to the file.
    """
    
    dir_name = os.path.dirname(file_name)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(file_name, 'a+') as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write('\n')
        file_object.write(text_to_append)
def printerror(**args):
    if 'm' in list(args.keys()):
        print(f"{get_time()}{Fore.RED}{Style.BRIGHT}Error: {args['m']}{Style.RESET_ALL}")
        append_new_line("logs/logs.txt",f"{get_time_blank()} ERROR: {args['m']}")
    else:
        print(f"{get_time()}{Fore.RED}{Style.BRIGHT}Error.{Style.RESET_ALL}")

    if 'name_of_data' in list(args.keys()) and 'data' in list(args.keys()) and 'm' in list(args.keys()):
        append_new_line("logs/logs.txt",f"{get_time_blank()} ERROR: {args['m']} | {args['name_of_data']}: {args['data']}")

    elif 'name_of_data' in list(args.keys()) and 'data' in list(args.keys()):
        append_new_line("logs/logs.txt",f"{get_time_blank()} ERROR | {args['name_of_data']}: {args['data']}")
def emergency_convert_list(pair_to_sell,exlist):
    i=0
    for echange in exlist:
        try:
            if ex[echange].has['cancelAllOrders'] and ex[echange].fetchOpenOrders(pair_to_sell) != []:
                ex[echange].cancelAllOrders(pair_to_sell)
                print(f"{get_time()} Successfully canceled all orders on {echange}.")
                append_new_line('logs/logs.txt',f"{get_time_blank()} INFO: successfully canceled all orders on {echange}.")
            bal = get_balance(echange,pair_to_sell)
            m = ex[echange].load_markets()
            t=ex[echange].fetch_ticker(pair_to_sell)
            m[pair_to_sell]['limits']['cost']['min'] = 0 if type(m[pair_to_sell]['limits']['cost']['min'])!=float and type(m[pair_to_sell]['limits']['cost']['min'])!=int else m[pair_to_sell]['limits']['cost']['min']
            m[pair_to_sell]['limits']['amount']['min'] = 0 if type(m[pair_to_sell]['limits']['amount']['min'])!=float and type(m[pair_to_sell]['limits']['amount']['min'])!=int else m[pair_to_sell]['limits']['amount']['min']
            m[pair_to_sell]['limits']['cost']['max'] = 10e13 if type(m[pair_to_sell]['limits']['cost']['max'])!=float and type(m[pair_to_sell]['limits']['cost']['max'])!=int else m[pair_to_sell]['limits']['cost']['max']
            m[pair_to_sell]['limits']['amount']['max'] = 10e13 if type(m[pair_to_sell]['limits']['amount']['max'])!=float and type(m[pair_to_sell]['limits']['amount']['max'])!=int else m[pair_to_sell]['limits']['amount']['max']
            if (bal>(m[pair_to_sell]['limits']['cost']['min']/float(t['last'])) and bal>m[pair_to_sell]['limits']['amount']['min']) and (bal<(m[pair_to_sell]['limits']['cost']['max']/float(t['last'])) and bal<m[pair_to_sell]['limits']['amount']['max']):
                ex[echange].createMarketSellOrder(symbol=pair_to_sell,amount=bal)
                print(f"{get_time()} Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
                append_new_line('logs/logs.txt',f"{get_time_blank()} INFO: Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            else: 
                print(f"{get_time()} Not enough {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
                append_new_line('logs/logs.txt',f"{get_time_blank()} INFO: Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            i+=1
        except Exception as e:
            printerror(m=f'{get_time()} Error while selling {pair_to_sell} on {echange}. Error: {e}',)
def printandtelegram(message):
    print(message)
    send_to_telegram(message)
def get_balance(exchange,symbol):
    if symbol[-5:] == '/USDT':
        symbol = symbol[:-5]
    balance=ex[exchange].fetch_balance()
    if balance[symbol]['free'] != 0:
        return balance[symbol]['free']
    else:
        return 0
    
ex = {n:getattr(ccxt,n)(exchanges[n]) for n in exchanges}

def get_precision_min(symbol,exchange_str):
    symbol_info = ex[exchange_str].load_markets(symbol)
    grail = symbol_info[symbol]['limits']['price']['min']
    return grail
def get_time():
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    dtf = now.strftime("[%d/%m/%Y  %H:%M:%S]")
    return f"{Style.DIM}{dtf}{Style.RESET_ALL}"
def get_time_blank():
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    dtf = now.strftime("[%d/%m/%Y  %H:%M:%S]")
    return dtf
def get_balance_usdt(ex_list_str:list):
    usdt_balance = 0
    for excha in ex_list_str:
        balances = ex[excha].fetchBalance()
        usdt_balance+=balances['USDT']['free']
    return float(usdt_balance)
