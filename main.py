import subprocess
import time
import sys
import os
from colorama import Style, init, Fore
init()
from exchange_config import *
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print("""
    █▄▄ ▄▀█ █▀█ █▄▄ █▀█ ▀█▀ █ █▄░█ █▀▀   ▄▀█ █▀█ █▄▄ █ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
    █▄█ █▀█ █▀▄ █▄█ █▄█ ░█░ █ █░▀█ ██▄   █▀█ █▀▄ █▄█ █ ░█░ █▀▄ █▀█ █▄█ ██▄   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█""")
print(f" \n{Fore.BLUE}{Style.BRIGHT}FAKE-MONEY VERSION{Style.RESET_ALL}\n \nLink for real money version: https://barbotine.capital/purchase-arbitrage\n \nGithub: nelso0\nTwitter: @nelsorex\nDiscord: nelsorex\n")
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
with open(f"start_balance.txt","w") as f:
    f.write(balance)
with open(f"balance.txt","w") as f:
    f.write(balance)

while True:
    if i>=1 and p.returncode==1:
        sys.exit(1)
    if mode == "fake-money":
        if len(args)<8:

            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Searching symbol... (can take some minutes)")
            p=subprocess.run([how_do_you_usually_launch_python, "best-symbol.py",ex1,ex2,ex3])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Crypto pair is: {symbol}")
            p=subprocess.run([how_do_you_usually_launch_python, "bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run([how_do_you_usually_launch_python,"bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()
    elif mode == "classic":
        if len(args)<8:

            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Searching symbol... (can take some minutes)")
            p=subprocess.run([how_do_you_usually_launch_python, "best-symbol.py",ex1,ex2,ex3])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Crypto pair is: {symbol}")
            p=subprocess.run([how_do_you_usually_launch_python, "bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run([how_do_you_usually_launch_python,"bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()
    elif mode == "delta-neutral":
        if len(args)<8:

            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Searching symbol... (can take some minutes)")
            p=subprocess.run([how_do_you_usually_launch_python, "best-symbol.py",ex1,ex2,ex3])
            with open('symbol.txt') as f:
                symbol=f.read()
            print(f"{Style.DIM}{get_time()}{Style.RESET_ALL} Crypto pair is: {symbol}")
            p=subprocess.run([how_do_you_usually_launch_python, "bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()

        if len(args)>=8:
            p=subprocess.run([how_do_you_usually_launch_python,"bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
            with open(f"balance.txt") as f:
                balance=f.read()
    else:
        print(f"Mode input is incorrect.")
        sys.exit(1)
    i+=1
