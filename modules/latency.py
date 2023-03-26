from exchange_config import *
import sys

echanges_str=[sys.argv[1],sys.argv[2],sys.argv[3]]
for exchange in echanges_str:
    try:
        time1 = time.time()
        ex[exchange].createLimitBuyOrder("BTC/USDT",999999,10000)
    except Exception as e:
        delay = int(round((time.time() - time1)*1000,0))
        print(f"{exchange} delay: {delay} ms")
