import ccxt as ccxt
import requests
import time

ex = {
    'kucoin':ccxt.kucoin({
        'apiKey':'here',
        'secret':'here',
        'password':'here'
    }),
    'binance':ccxt.binance({
        'apiKey':'here',
        'secret':'here',
    }),
    'okx':ccxt.okx({
        'apiKey':'here',
        'secret':'here',
        'password':'here'
    }),
    
    # 'another_exchange_here':ccxt.other_exchange({
    #     'apiKey':'here',
    #     'secret':'here',
    # }),
}

fees = { # put maker fees of your exchanges in 'receive' (only if it's a quote and not base fee)
    'binance' : {'receive':0.001},
    'kucoin' : {'receive':0.001},
    'okx' : {'receive':0.0008},
    'another_exchange_here' : {'receive':0},
}

telegram_sending = False
apiToken = 'here' # telegram API to send everything to you, don't fill if you don't want telegram (False = not activated by default)
chatID = 'here'

first_orders_fill_timeout = 0 # ONLY FOR FULL VERSION       # if equals to 0 = no timeout, check indefinitely to fill first orders. Put a value for the timeout in seconds if you want to have a timeout.

criteria_pct = 0 # minimum of profits to take the opportunity, default to 0 so it takes the opportunity even if this is a 0.001 USD profit. (all fees are already included in the calculation, so it's actual profit)
criteria_usd = 0

def moy(list):
    moy=0
    for n in list:
        moy+=n
    return moy/len(list)
def send_to_telegram(message):
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
