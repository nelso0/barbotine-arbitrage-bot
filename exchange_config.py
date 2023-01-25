import ccxt.pro as ccxtpro
import ccxt as ccxt
import requests
import time

ex = {
    'kucoinfutures':ccxt.kucoinfutures({ # for delta-neutral mode
        'password':'here',
        'apiKey':'here',
        'secret':'here',
    }),
    'kucoin':ccxt.kucoin({
        'password':'here',
        'apiKey':'here',
        'secret':'here',
    }),
    'binance':ccxt.binance({
        'apiKey':'here',
        'secret':'here',
    }),
    'okx':ccxt.okx({
        'password':'here',
        'apiKey':'here',
        'secret':'here',
    }),
    # same 3 here
    'kucoinpro':ccxtpro.kucoin({
        'password':'here',
        'apiKey':'here',
        'secret':'here',
    }),
    'binancepro':ccxtpro.binance({
        'apiKey':'here',
        'secret':'here',
    }),
    'okxpro':ccxtpro.okx({
        'password':'here',
        'apiKey':'here',
        'secret':'here',
    })
}

echanges_str = ["binance","kucoin","okx"]
echanges = [ex['binance'],ex['kucoin'],ex['okx']]


fees = { # maker fees
    'binance' : {'give':0,"receive":0.001},
    'kucoin' : {'give':0,"receive":0.001},
    'okx' : {'give':0,"receive":0.0008},
}

# telegram API to send everything to you

apiToken = '5936932624:AAF5v1wyDZIRZsYKjmiqMUzoSnzLBuZaZ1c'
chatID = '5198472708'

# minimum of profits to take the opportunity
# default to 0 so it takes the opportunity even if this is a 0.001 USD profit. (all fees are already included in the calculation, so it's actual profit)

criteria_pct = 0
criteria_usd = 0

# some useful functions here

def moy(list):
    moy=0
    for n in list:
        moy+=n
    return moy/len(list)
def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    except Exception as e:
        print(e)
def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.turtle.write("\n")
        file_object.turtle.write(text_to_append)
def printandtelegram(message):
    print(message)
    send_to_telegram(message)
def emergency_convert(pair_to_sell):
    i=0
    for echange in echanges_str:
        try:
            if ex[echange].has['cancelAllOrders'] and ex[echange].fetchOpenOrders(pair_to_sell) != []:
                ex[echange].cancelAllOrders(pair_to_sell)
                print(f"Successfully canceled all orders on {echange}.")
            bal = get_balance(echange,pair_to_sell)
            if echange == "okx":
                bal-=bal*0.02
            if echange == "kucoin":
                bal-=bal*0.015
            if bal>(float(10)/float(ex[echange].fetch_ticker(pair_to_sell)['last'])):
                ex[echange].createMarketSellOrder(symbol=pair_to_sell,amount=round(bal,3))
                print(f"Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            else: print(f"Not enough {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            i+=1
        except Exception as e:
            print(f'Problem on {echange}. Error:    {e}')
def get_balance(exchange,symbol):
    if symbol[-5:] == '/USDT':
        symbol = symbol[:-5]
    balance=ex[exchange].fetch_balance()
    if symbol in balance["free"] != 0:
        return balance['free'][symbol]
    else: return 0