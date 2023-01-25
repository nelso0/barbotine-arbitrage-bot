from asyncio import gather, run
import time
import random
import os
import requests
import ccxt.pro
import ccxt
import sys
from colorama import Fore, Back, Style
from exchange_config import *
bid_prices = {}
ask_prices = {}
total_absolute_profit_pct=0
prec_ask_price = 0
prec_bid_price = 0
i=0
z=0
if len(sys.argv) != 5:
    print(f" \nUsage: $ python3 bot-fake-money.py [pair] [total_usdt_investment] [stop.delay.minutes] [tlgrm.msg.title]\n ")
    sys.exit(1)
print(" ")

kucoinPair = str(sys.argv[1])
howmuchusd = float(sys.argv[2])
inputtimeout = int(sys.argv[3])*60
indicatif = str(sys.argv[4])
timeout = time.time() + inputtimeout

s=0

usd = {exchange:(howmuchusd/2)/len(echanges) for exchange in echanges_str}

total_usd = usd['binance'] + usd['kucoin'] + usd['okx']

all_tickers = []

try:
    printandtelegram(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Fetching the global average price for {kucoinPair}...")
    for exchange in echanges:
        ticker = exchange.fetch_ticker(kucoinPair)
        all_tickers.append(ticker['bid'])
        all_tickers.append(ticker['ask'])
    average_first_buy_price = moy(all_tickers)
    total_crypto = (howmuchusd/2)/average_first_buy_price
    printandtelegram(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Average {kucoinPair} price in USDT: {average_first_buy_price}")
    printandtelegram(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] If that was with real money, orders would be sent here for {round(total_crypto/len(echanges),3)} {kucoinPair[:-5]} at {average_first_buy_price}.")

except Exception as e:
    print(f"Error while fetching orders. Error: {e}")
    for exchange in ex:
        exchange.close()

crypto = {exchange:total_crypto/len(echanges) for exchange in echanges_str}

i=0

crypto_per_transaction = total_crypto/len(echanges_str)

printandtelegram(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Starting program with parameters: {[n for n in sys.argv]}")
prec_time = '0000000'
min_ask_price = 0

async def symbol_loop(exchange, symbol):
    global total_crypto,crypto_per_transaction,i,z,prec_time,t,time1,bid_prices,ask_prices,total_absolute_profit_pct,min_ask_price,max_bid_price,prec_ask_price,prec_bid_price,timeout,profit_pct,profit_usd
    while time.time() <= timeout:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()
            bid_prices[exchange.id] = orderbook["bids"][0][0]
            ask_prices[exchange.id] = orderbook["asks"][0][0]
            min_ask_ex = min(ask_prices, key=ask_prices.get)
            max_bid_ex = max(bid_prices, key=bid_prices.get)
            for n in echanges_str:
                if crypto[n] < crypto_per_transaction:
                    min_ask_ex = n
                if usd[n] <= 0: # should not happen
                    max_bid_ex = n
            min_ask_price = ask_prices[min_ask_ex]
            max_bid_price = ask_prices[max_bid_ex]
            profit_usd = (min_ask_price*((total_crypto/len(echanges_str)))*((max_bid_price-min_ask_price)/min_ask_price))
            profit_pct = profit_usd/(0.01*total_usd)
            profit_with_fees_usd = profit_usd - (((crypto_per_transaction) * max_bid_price)*(fees[max_bid_ex]['receive']) + ((crypto_per_transaction * min_ask_price)*(fees[min_ask_ex]['give'])))
            profit_with_fees_pct = ((profit_with_fees_usd/total_usd)*100)/2

            if max_bid_ex != min_ask_ex and profit_with_fees_usd > float(criteria_usd) and profit_with_fees_pct > float(criteria_pct) and prec_ask_price != min_ask_price and prec_bid_price != max_bid_price and usd[min_ask_ex] >= crypto_per_transaction * min_ask_price * (1+fees[min_ask_ex]['give']) and crypto[max_bid_ex] >= crypto_per_transaction * (1+fees[max_bid_ex]['give']):
                i+=1
                
                crypto[min_ask_ex] += crypto_per_transaction * (1-fees[min_ask_ex]['receive'])
                usd[min_ask_ex] -= crypto_per_transaction * min_ask_price * (1+fees[min_ask_ex]['give'])
                crypto[max_bid_ex] -= crypto_per_transaction * (1+fees[max_bid_ex]['give'])
                usd[max_bid_ex] += crypto_per_transaction * max_bid_price * (1+fees[max_bid_ex]['receive'])

                total_fees_crypto = crypto_per_transaction * (fees[max_bid_ex]['give']) + (crypto_per_transaction * (fees[min_ask_ex]['receive']))
                total_fees_usd = ((crypto_per_transaction) * max_bid_price)*(fees[max_bid_ex]['receive']) + ((crypto_per_transaction * min_ask_price)*(fees[min_ask_ex]['give']))

                total_absolute_profit_pct += profit_with_fees_pct

                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print(" \n-----------------------------------------------------\n")

                print(f"{Style.RESET_ALL}Opportunity n°{i} detected! ({min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex})\n \nProfit: {Fore.GREEN}+{round(profit_with_fees_pct,4)} % (+{round(profit_with_fees_usd,4)} USD){Style.RESET_ALL}\n \nSession total profit: {Fore.GREEN}+{round(total_absolute_profit_pct,4)} %     (+{round((total_absolute_profit_pct/100)*howmuchusd,4)} USD){Style.RESET_ALL}\n \nFees: {Fore.RED}-{round(total_fees_usd,4)} USD      -{round(total_fees_crypto,4)} {kucoinPair[:len(kucoinPair)-5]}\n \n{Style.RESET_ALL}Current worth: {round((howmuchusd*(1+(total_absolute_profit_pct/100))),3)} USD{Style.RESET_ALL}{Style.DIM}\n \n➝ binance: {round(crypto['binance'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['binance'],2)} USDT\n➝ kucoin: {round(crypto['kucoin'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['kucoin'],2)} USDT\n➝ okx: {round(crypto['okx'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['okx'],2)} USDT\n \nTime elapsed since the beginning of the session: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\n \n{Style.RESET_ALL}-----------------------------------------------------\n \n")
                send_to_telegram(f"[{indicatif} Trade n°{i}]\n \nOpportunity detected!\n \nProfit: {round(profit_with_fees_pct,4)} % ({round(profit_with_fees_usd,4)} USD)\n \n{min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex}\nTime elapsed: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\nSession total profit: {round(total_absolute_profit_pct,4)} % ({round((total_absolute_profit_pct/100)*howmuchusd,4)} USDT)\nTotal fees paid on this session: {round(total_fees_usd,4)} USD      {round(total_fees_crypto,4)} {kucoinPair[:len(kucoinPair)-5]}\n \n--------BALANCES---------\n \nCurrent worth: {round((howmuchusd*(1+(total_absolute_profit_pct/100))),3)} USD\n \n➝ binance: {round(crypto['binance'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['binance'],2)} USDT\n➝ kucoin: {round(crypto['kucoin'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['kucoin'],2)} USDT\n➝ okx: {round(crypto['okx'],3)} {kucoinPair[:len(kucoinPair)-5]} / {round(usd['okx'],2)} USDT\n \n")
            
                prec_ask_price = min_ask_price
                prec_bid_price = max_bid_price

                total_crypto = crypto["binance"]+crypto["kucoin"]+crypto["okx"]
                crypto_per_transaction = total_crypto/len(echanges_str)
            else:
                for count in range(0,1):
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                if profit_with_fees_usd < 0:
                    color = Fore.RED
                elif profit_with_fees_usd > 0:
                    color = Fore.GREEN
                elif profit_with_fees_usd == 0:
                    color = Fore.WHITE
                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Best opportunity: {color}{round(profit_with_fees_usd,4)} USD {Style.RESET_ALL}(with fees)       buy: {min_ask_ex} at {min_ask_price}     sell: {max_bid_ex} at {max_bid_price}")
            time1=exchange.iso8601(exchange.milliseconds())
            if time1[17:19] == "00" and time1[14:16] != prec_time:
                prec_time = time1[11:13]
                await exchange.close()
            z+=1

        except Exception as e:
            print(str(e))
            await exchange.close()
            break

async def exchange_loop(exchange_id, symbols):
    exchange = getattr(ccxt.pro, exchange_id)()
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

async def main():
    exchanges = {
        "kucoin": [kucoinPair],
        "binance": [kucoinPair],
        "okx":[kucoinPair]
    }
    loops = [
        exchange_loop(exchange_id, symbols)
        for exchange_id, symbols in exchanges.items()
    ]
    await gather(*loops)

st = time.time()
print(" \n")
run(main())
with open('balance.txt', 'r+') as balance_file:
    balance = float(balance_file.read())
    balance_file.seek(0)
    balance_file.write(str(round(balance * (1 + (total_absolute_profit_pct/100)), 3)))
    balance = float(round(balance * (1 + (total_absolute_profit_pct/100)), 3))
printandtelegram(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Session with {kucoinPair} finished.\nTotal profit: {round(total_absolute_profit_pct,4)} % ({round((total_absolute_profit_pct/100)*howmuchusd,4)} USDT)\n \nTotal current balance: {balance} USDT")

