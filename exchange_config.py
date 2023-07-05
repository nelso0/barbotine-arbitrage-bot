import ccxt as ccxt
import requests
import time
import pytz
import datetime

telegram_sending = False
ctrl_c_handling = True

how_do_you_usually_launch_python = 'python' # the command you put in the terminal/cmd to launch python. Usually: python, python3, py...

ex = {
    'kucoin':ccxt.kucoin(),
    'binance':ccxt.binance(),
    'okx':ccxt.okx(),
    # for delta-neutral full version only
        #'kucoinfutures':ccxt.kucoinfutures({
        #'apiKey':'here',
        #'secret':'here',
        #'password':'here'
    # }),
    # 'another_exchange_here':ccxt.other_exchange({
    #     'apiKey':'here',
    #     'secret':'here',
    # }),
}

apiToken = 'here' # telegram API to send everything to you, don't fill if you don't want telegram (False = not activated by default)
chatID = 'here'

criteria_pct = 0 # minimum of price difference in % to take the opportunity
criteria_usd = 0

def moy(list):
    moy=0
    for n in list:
        moy+=n
    return moy/len(list)
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
    if symbol in balance['free'] != 0:
        return balance['free'][symbol]
    else: return 0
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
