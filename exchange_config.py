import ccxt as ccxt
import requests
import time
import pytz
import datetime

# The bot seems complicated? I swear it's not, just try! (and contact me if you have an error, it's probably a silly one :)

telegram_sending = False
ctrl_c_handling = True
renewal = False # you can enable session renewal here, default: False

how_do_you_usually_launch_python = 'python3' # the command you put in the terminal/cmd to launch python. Usually: python, python3, py...

# you have to put your api keys if you want to use real money modes. To do that, add "{'apiKey':'here','secret':'here'}" between the parenthesis () by replacing 'here' with the api key and the secret key.
# read the instructions on the google drive link you received for more details and screenshots.
ex = {
    'kucoin':ccxt.kucoin(),
    'binance':ccxt.binance(),
    'okx':ccxt.okx(),
    'poloniex':ccxt.poloniex(),
    # 'another_exchange_here':ccxt.other_exchange({
    #     'apiKey':'here',
    #     'secret':'here',
    # }),
}

apiToken = 'here' # telegram API to send everything to you, don't fill if you don't want telegram
chatID = 'here'

first_orders_fill_timeout = 0 # put a value for the timeout in minutes. 0 means desactivated (default)

criteria_pct = 0 # minimum of price difference in % to take the opportunity
criteria_usd = 0

def moy(list1):
    moy=0
    for n in list1:
        moy+=n
    return moy/len(list1)
def send_to_telegram(message):
    message = message.replace("[2m","")
    message = message.replace("[0m","")
    message = message.replace("[2m","")
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
    with open(file_name, 'a+') as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.turtle.write('\n')
        file_object.turtle.write(text_to_append)
def printandtelegram(message):
    print(message)
    send_to_telegram(message)
def get_balance(exchange,symbol):
    if symbol[-5:] == '/USDT':
        symbol = symbol[:-5]
    balance=ex[exchange].fetch_balance()
    if balance[symbol]['total'] != 0:
        return balance[symbol]['total']
    else:
        return 0
def get_precision_min(symbol,exchange_str):
    symbol_info = ex[exchange_str].load_markets(symbol)
    graal = symbol_info[symbol]['limits']['price']['min']
    return graal
def get_time():
    # Définir la timezone française
    tz_france = pytz.timezone('Europe/Paris')

    # Obtenir la date et l'heure actuelles dans la timezone française
    now = datetime.datetime.now(tz_france)

    # Formater la date et l'heure dans le format souhaité
    date_heure_format = now.strftime("[%d/%m/%Y  %H:%M:%S]")

    # Retourner la date et l'heure formatées
    return date_heure_format
def get_balance_usdt(ex_list_str:list):
    usdt_balance = 0
    for excha in ex_list_str:
        balances = ex[excha].fetchBalance()
        usdt_balance+=balances['USDT']['total']
    return float(usdt_balance)
