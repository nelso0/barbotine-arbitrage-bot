import subprocess
import time
import sys
import os

print("""
█▄▄ ▄▀█ █▀█ █▄▄ █▀█ ▀█▀ █ █▄░█ █▀▀   ▄▀█ █▀█ █▄▄ █ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
█▄█ █▀█ █▀▄ █▄█ █▄█ ░█░ █ █░▀█ ██▄   █▀█ █▀▄ █▄█ █ ░█░ █▀▄ █▀█ █▄█ ██▄   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█""")

print(" \nUnder Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license, for personal-use only.\n \nGithub: nelso0\nTwitter: @nelsodot\n")

args = sys.argv
mode = args[1]
balance = args[3]
if len(args)>=8:
    symbol=args[7]
renew=args[2]
ex1=args[4]
ex2=args[5]
ex3=args[6]
i=0
with open(f"start_balance-{balance}.txt","w") as f:
    f.write(balance)
with open(f"balance-{balance}.txt","w") as f:
    f.write(balance)

while True:
    if i>=1 and p.returncode==1:
        sys.exit(1)
    if mode == "fake-money":
        if len(args)<8:

            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Searching symbol... (can take some minutes)")
            p=subprocess.run(['python', "best-symbol.py"])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
            p=subprocess.run(['python', "bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run(['python',"bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()
    elif mode == "classic":
        if len(args)<8:

            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Searching symbol... (can take some minutes)")
            p=subprocess.run(['python', "best-symbol.py"])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
            p=subprocess.run(['python', "bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run(['python',"bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()
    elif mode == "delta-neutral":
        if len(args)<8:

            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Searching symbol... (can take some minutes)")
            p=subprocess.run(['python', "best-symbol.py"])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
            p=subprocess.run(['python', "bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run(['python',"bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance-{balance}.txt") as f:
                balance=f.read()
    else:
        print(f"Mode input is incorrect.")
        sys.exit(1)
    i+=1
