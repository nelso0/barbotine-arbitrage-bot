import subprocess
import os
import sys
import time
from os import path

if len(sys.argv) < 2:
    input_list = ["mode (fake-money, classic, delta-neutral)", "renew time (in minutes)", "balance to use (USDT)", "exchange 1","exchange 2","exchange 3","crypto pair (put nothing if you want it to be automatically selected)"]
    output = []
    
    for inputt in input_list:
        output.append(input(inputt+" >>> "))

    if output[6]=='':
        subprocess.run(['python3',f"main.py",output[0],output[1],output[2],output[3],output[4],output[5]])
    else:
        subprocess.run(['python3',f"main.py",output[0],output[1],output[2],output[3],output[4],output[5],output[6]])

else:
    print("""
█▄▄ ▄▀█ █▀█ █▄▄ █▀█ ▀█▀ █ █▄░█ █▀▀   ▄▀█ █▀█ █▄▄ █ ▀█▀ █▀█ ▄▀█ █▀▀ █▀▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
█▄█ █▀█ █▀▄ █▄█ █▄█ ░█░ █ █░▀█ ██▄   █▀█ █▀▄ █▄█ █ ░█░ █▀▄ █▀█ █▄█ ██▄   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█""")
    print(" \nUnder Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license, for personal-use only.\n \nGithub: nelso0\nTwitter: @nelsodot\n")
    if len(sys.argv) < 7 or len(sys.argv) > 8:
        print("Not correctly configured. Usage:\n \npython run.py <mode> <symbol-renew-time> <usdt-to-use> <exchange1> <exchange2> <exchange3> [crypto-pair]\n")
        sys.exit(1)
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
                p=subprocess.run(['python3', "best-symbol.py"])
                with open('symbol.txt') as f:
                    symbol=f.read()
                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
                p=subprocess.run(['python3', "bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()

            if len(args)>=8:
                p=subprocess.run(['python3',"bot-fake-money.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()
        elif mode == "classic":
            if len(args)<8:

                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Searching symbol... (can take some minutes)")
                p=subprocess.run(['python3', "best-symbol.py"])
                with open('symbol.txt') as f:
                    symbol=f.read()
                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
                p=subprocess.run(['python3', "bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()

            if len(args)>=8:
                p=subprocess.run(['python3',"bot-classic.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()
        elif mode == "delta-neutral":
            if len(args)<8:

                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Searching symbol... (can take some minutes)")
                p=subprocess.run(['python3', "best-symbol.py"])
                with open('symbol.txt') as f:
                    symbol=f.read()
                print(f"[{time.strftime('%H:%M:%S', time.gmtime(time.time()))}] Crypto pair is: {symbol}")
                p=subprocess.run(['python3', "bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()

            if len(args)>=8:
                p=subprocess.run(['python3',"bot-delta-neutral.py",symbol,balance,renew,symbol,ex1,ex2,ex3])
                with open(f"balance-{balance}.txt") as f:
                    balance=f.read()
        else:
            print(f"Mode input is incorrect.")
            sys.exit(1)
        i+=1



