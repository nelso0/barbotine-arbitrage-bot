# it's sloppy; needs serious improvement.
import time
from exchange_config import *
st = time.time()
binancePairs = []
marketsBinance = ex['binance'].load_markets()
for m in marketsBinance:
    binancePairs.append(m)
kucoinPairs = []
marketsKucoin = ex['kucoin'].load_markets()
for m in marketsKucoin:
    kucoinPairs.append(m)
OkxPairs = []
marketsOKX = ex['okx'].load_markets()
for m in marketsOKX:
    OkxPairs.append(m)
OKXset = set(OkxPairs)
Binanceset = set(binancePairs)
Kucoinset = set(kucoinPairs)
if (OKXset & Binanceset & Kucoinset):
    list1 = list(OKXset & Binanceset & Kucoinset)
list2 = []
for n in list1:
    ticker = ex['binance'].fetch_ticker(n)
    if n[-4:] == 'USDT' and float(ticker["info"]["volume"])*float(ticker["last"])>1200000 and n!='MIR/USDT':
        list2.append(n)
        time.sleep(1)
finalDic={}
for x in list2:
    pct = round((ex['binance'].fetch_ticker(x)['percentage']+ex['kucoin'].fetch_ticker(x)['percentage']+ex['okx'].fetch_ticker(x)['percentage'])/3,3)
    finalDic[x] = pct
max_pct = max([finalDic[n] for n in finalDic])
max_symbol = list(finalDic.keys())[list(finalDic.values()).index(max_pct)]
balance_file = open('symbol.txt','w')
balance_file.write(max_symbol)
