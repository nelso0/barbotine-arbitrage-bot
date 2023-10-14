from asyncio import gather, run
import time
import ccxt.pro
import ccxt
import sys
from colorama import Fore, Back, Style,init
init()
from exchange_config import *
bid_prices = {}
ask_prices = {}
total_change_usd = 0
total_change_usd_pct = 0
prec_ask_price = 0
prec_bid_price = 0
i=0
z=0
if len(sys.argv) != 6:
    print(f" \nIncorrect usage, this is what it has to look like: $ {how_do_you_usually_launch_python} bot-classic.py [pair] [total_usdt_investment] [stop.delay.minutes] [tlgrm.msg.title] [ex_list]\n ")
    print(f" \n This is the list of args you wrote: {sys.argv}")
    sys.exit(1)
print(" ")
if first_orders_fill_timeout <= 0:
    first_orders_fill_timeout = 3600 # 2.5 days
print(f" \n This is the list of args you wrote: {sys.argv}")
echanges = [ex[sys.argv[5].split(',')[i]] for i in range(len(sys.argv[5].split(',')))]
echanges_str = [sys.argv[5].split(',')[i] for i in range(len(sys.argv[5].split(',')))]
currentPair = str(sys.argv[1])
criteria_usd = str(criteria_usd)
criteria_pct = str(criteria_pct)
howmuchusd = float(sys.argv[2])
inputtimeout = int(sys.argv[3])*60
indicatif = str(sys.argv[4])
timeout = time.time() + inputtimeout
endPair = currentPair.split('/')[1]

def emergency_convert(pair_to_sell):
    i=0
    for echange in echanges_str:
        try:
            if ex[echange].has['cancelAllOrders'] and ex[echange].fetchOpenOrders(pair_to_sell) != []:
                ex[echange].cancelAllOrders(pair_to_sell)
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully canceled all orders on {echange}.")
            bal = get_balance(echange,pair_to_sell)
            if bal>(float(10)/float(ex[echange].fetch_ticker(pair_to_sell)['last'])):
                ex[echange].createMarketSellOrder(symbol=pair_to_sell,amount=bal)
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            else: print(f"Not enough {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            i+=1
        except Exception as e:
            print(f'{Style.DIM}[{time.strftime("%H:%M:%S", time.gmtime(time.time()))}]{Style.RESET_ALL} Problem on {echange}. Error:    {e}')           
def emergency_convert_list(pair_to_sell,exlist):
    i=0
    for echange in exlist:
        try:
            if ex[echange].has['cancelAllOrders'] and ex[echange].fetchOpenOrders(pair_to_sell) != []:
                ex[echange].cancelAllOrders(pair_to_sell)
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully canceled all orders on {echange}.")
            bal = get_balance(echange,pair_to_sell)
            if bal>(float(10)/float(ex[echange].fetch_ticker(pair_to_sell)['last'])):
                ex[echange].createMarketSellOrder(symbol=pair_to_sell,amount=bal)
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Successfully sold {bal} {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            else: print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Not enough {pair_to_sell[:len(pair_to_sell)-5]} on {echange}.")
            i+=1
        except Exception as e:
            print(f'{Style.DIM}[{time.strftime("%H:%M:%S", time.gmtime(time.time()))}]{Style.RESET_ALL} Problem on {echange}. Error:    {e}')

s=0

ordersFilled = 0

while ordersFilled != len(echanges):

    if s==1:
        sys.exit(1)
    usd = {exchange:(howmuchusd/2)/len(echanges) for exchange in echanges_str}

    total_usd = 0
    for exc in echanges_str:
        total_usd+=usd[exc]

    all_tickers = []

    try:
        printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Fetching the global average price for {currentPair}...")
        for n in echanges:
            ticker = n.fetch_ticker(currentPair)
            all_tickers.append(ticker['last'])
        average_first_buy_price = moy(all_tickers)
        total_crypto = (howmuchusd/2)/average_first_buy_price
        printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Average {currentPair} price in {endPair}: {average_first_buy_price}")

    except Exception as e:
        print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Error while fetching average prices. Error: {e}")
        for exc in echanges_str:
            ex[exc].close()

    crypto = {exchange:total_crypto/len(echanges) for exchange in echanges_str}

    crypto_per_transaction = (total_crypto/len(echanges_str))

    i=0
    for n in echanges:
        time.sleep(0.7)
        printandtelegram(f'{Style.DIM}{get_time()}{Style.RESET_ALL} Buy limit order of {round(total_crypto/len(echanges),3)} {currentPair.split("/")[0]} at {average_first_buy_price} sent to {echanges_str[i]}.')
        i+=1

    printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} All orders sent.")

    already_filled = []
    for zz in range(len(echanges)):
        time.sleep(2.1)
        printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} {echanges_str[zz]} order filled.")
        ordersFilled+=1
        already_filled.append(exc)

printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Starting program with parameters: {[n for n in sys.argv]}")
prec_time = '0000000'
min_ask_price = 0
total_change_usd_pct=0
total_change_usd=0
async def symbol_loop(exchange, symbol):
    global total_change_usd,total_change_usd_pct,crypto_per_transaction,i,z,prec_time,t,time1,bid_prices,ask_prices,total_absolute_profit_pct,min_ask_price,max_bid_price,prec_ask_price,prec_bid_price,timeout,profit_pct,profit_usd,total_crypto
    while time.time() <= timeout:
        # try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()
            bid_prices[exchange.id] = orderbook["bids"][0][0]
            ask_prices[exchange.id] = orderbook["asks"][0][0]
            min_ask_ex = min(ask_prices, key=ask_prices.get)
            max_bid_ex = max(bid_prices, key=bid_prices.get)
            for u in echanges_str:
                if crypto[u] < crypto_per_transaction:
                    min_ask_ex = u
                if usd[u] <= 0: # should not happen
                    max_bid_ex = u
            min_ask_price = ask_prices[min_ask_ex]
            max_bid_price = bid_prices[max_bid_ex]

            theoritical_min_ask_usd_bal = usd[min_ask_ex] - (crypto_per_transaction / (1-fees[min_ask_ex]['quote'])) * min_ask_price * (1+fees[min_ask_ex]['base'])
            theoritical_max_bid_usd_bal = usd[max_bid_ex] + (crypto_per_transaction / (1+fees[max_bid_ex]['base']) * max_bid_price * (1-fees[max_bid_ex]['quote']))

            change_usd = (theoritical_min_ask_usd_bal+theoritical_max_bid_usd_bal)-(usd[max_bid_ex]+usd[min_ask_ex])
            total_usd_balance = 0
            for n in echanges_str:
                total_usd_balance+=usd[n]
            change_usd_pct = (change_usd/total_usd_balance)*100

            if max_bid_ex != min_ask_ex and change_usd > float(criteria_usd) and change_usd_pct > float(criteria_pct) and prec_ask_price != min_ask_price and prec_bid_price != max_bid_price:
                i+=1
                
                fees_crypto = crypto_per_transaction * (fees[min_ask_ex]['quote']) + crypto_per_transaction * (fees[max_bid_ex]['base'])
                fees_usd = crypto_per_transaction * max_bid_price * (fees[max_bid_ex]['quote']) + crypto_per_transaction * min_ask_price * (fees[min_ask_ex]['base'])

                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print("-----------------------------------------------------\n")
                
                ex_balances = ""
                for exc in echanges_str:
                    ex_balances+=f"\n➝ {exc}: {round(crypto[exc],3)} {currentPair.split('/')[0]} / {round(usd[exc],2)} {endPair}"
                print(f"{Style.RESET_ALL}Opportunity n°{i} detected! ({min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex})\n \nExcepted profit: {Fore.GREEN}+{round(change_usd_pct,4)} % (+{round(change_usd,4)} {endPair}){Style.RESET_ALL}\n \nSession total profit: {Fore.GREEN}+{round(total_change_usd_pct,4)} %     (+{round((total_change_usd/100)*howmuchusd,4)} {endPair}){Style.RESET_ALL}\n \nFees paid: {Fore.RED}-{round(fees_usd*max_bid_price,4)} {endPair}      -{round(fees_crypto,4)} {currentPair.split('/')[0]}\n \n{Style.RESET_ALL}{Style.DIM} {ex_balances}\n \n{Style.RESET_ALL}Time elapsed since the beginning of the session: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\n \n{Style.RESET_ALL}-----------------------------------------------------\n \n")
                send_to_telegram(f"[{indicatif} Trade n°{i}]\n \nOpportunity detected!\n \nExcepted profit: {round(change_usd_pct,4)} % ({round(change_usd,4)} {endPair})\n \n{min_ask_ex} {min_ask_price}   ->   {max_bid_price} {max_bid_ex}\nTime elapsed: {time.strftime('%H:%M:%S', time.gmtime(time.time()-st))}\nSession total profit: {round(total_change_usd_pct,4)} % ({round(total_change_usd,4)} {endPair})\nFees paid: {round(fees_usd*max_bid_price,4)} {endPair}      {round(fees_crypto,4)} {currentPair.split('/')[0]}\n \n--------BALANCES---------\n \n {ex_balances}")

                printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Sell market order filled on {max_bid_ex} for {crypto_per_transaction} {currentPair.split('/')[0]} at {max_bid_price}.")
                printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Buy market order filled on {max_bid_ex} for {crypto_per_transaction} {currentPair.split('/')[0]} at {min_ask_price}.")

                append_list_file('all_opportunities_profits.txt',change_usd_pct)

                crypto[min_ask_ex] += crypto_per_transaction
                usd[min_ask_ex] -= (crypto_per_transaction / (1-fees[min_ask_ex]['quote'])) * min_ask_price * (1+fees[min_ask_ex]['base'])
                crypto[max_bid_ex] -= crypto_per_transaction
                usd[max_bid_ex] += crypto_per_transaction / (1+fees[max_bid_ex]['base']) * max_bid_price * (1-fees[max_bid_ex]['quote'])

                total_change_usd+=change_usd
                total_change_usd_pct+=change_usd_pct

                prec_ask_price = min_ask_price
                prec_bid_price = max_bid_price

                total_crypto = 0
                for exc in echanges_str:
                    total_crypto+=crypto[exc]
                crypto_per_transaction = total_crypto/len(echanges_str)
            
            else:
                for count in range(0,1):
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                if change_usd < 0:
                    color = Fore.RED
                elif change_usd > 0:
                    color = Fore.GREEN
                elif change_usd == 0:
                    color = Fore.WHITE
                print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Best opportunity: {color}{round(change_usd,4)} {endPair} {Style.RESET_ALL}(with fees)       buy: {min_ask_ex} at {min_ask_price}     sell: {max_bid_ex} at {max_bid_price}")
            time1=exchange.iso8601(exchange.milliseconds())
            if time1[17:19] == "00" and time1[14:16] != prec_time:
                prec_time = time1[11:13]
                await exchange.close()

        # except Exception as e:
        #     print(str(e))
        #     break  # you can break just this one loop if it fails

async def exchange_loop(exchange_id, symbols):
    exchange = getattr(ccxt.pro, exchange_id)()
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

async def main():
    exchanges = {
        echanges_str[i]:[currentPair] for i in range(0,len(echanges))
    }
    loops = [
        exchange_loop(exchange_id, symbols)
        for exchange_id, symbols in exchanges.items()
    ]
    await gather(*loops)

st = time.time()
print(" \n")
run(main())

for exc in crypto:
    ticker = ex[exc].fetchTicker(currentPair)
    price = ticker['last']
    usd[exc]+=((crypto[exc])*(1-fees[exc]['base'])*price)*(1-fees[exc]['quote'])
    crypto[exc]=0

total_usdt_balance = 0
for n in echanges_str:
    total_usdt_balance += usd[n]
with open('balance.txt', 'r+') as balance_file:
    old_balance = float(balance_file.read())
    balance_file.seek(0)
    balance_file.write(str(total_usdt_balance))

total_session_profit_usd = total_usdt_balance-old_balance
total_session_profit_pct = (total_session_profit_usd/old_balance)*100
printandtelegram(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Session with {currentPair} finished.\n{Style.DIM}{get_time()}{Style.RESET_ALL} Total profit: {round(total_session_profit_pct,4)} % ({total_session_profit_usd} {endPair})")
