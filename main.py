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
print(f" \n{Fore.BLUE}{Style.BRIGHT}DEMO VERSION{Style.RESET_ALL}\n \nnelsorex\nTwitter: @nelsorex\nDiscord: nelsorex\n")
args = sys.argv
mode = args[1]
if renewal:
    balance = args[3]
    symbol=args[4]
    renew=args[2]
    ex_list=args[5]
else:
    balance = args[2]
    symbol=args[3]
    renew="525600"
    ex_list=args[4]
i=0
with open(f"start_balance.txt","w") as f:
    f.write(balance)
with open(f"balance.txt","w") as f:
    f.write(balance)

while True:
    if i>=1 and p.returncode==1:
        sys.exit(1)
    if mode == "fake-money":
        p=subprocess.run([how_do_you_usually_launch_python,"bot-fake-money.py",symbol,balance,renew,symbol,ex_list])
        with open(f"balance.txt") as f:
            balance=f.read()
    elif mode == "classic":
        p=subprocess.run([how_do_you_usually_launch_python,"bot-classic.py",symbol,balance,renew,symbol,ex_list])
        with open(f"balance.txt") as f:
            balance=f.read()
    elif mode == "delta-neutral":
        p=subprocess.run([how_do_you_usually_launch_python,"bot-delta-neutral.py",symbol,balance,renew,symbol,ex_list])
        with open(f"balance.txt") as f:
            balance=f.read()
    else:
        print(f"Mode input is incorrect.")
        sys.exit(1)
    i+=1
