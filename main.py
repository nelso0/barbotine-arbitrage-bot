import subprocess
import time
import sys,ccxt
import os
from colorama import Style, init, Fore
init()
from exchange_config import *
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print('''
                                                                                                                     
                                                                                                                     
VMA""YMM      `7MM"""Yp,      db      `7MM"""Mq.  `7MM"""Yp,   .g8""8q.  MMP""MM""YMM `7MMF'`7MN.   `7MF'`7MM"""YMM  
 VMA  `7        MM    Yb     ;MM:       MM   `MM.   MM    Yb .dP'    `YM.P'   MM   `7   MM    MMN.    M    MM    `7  
  VMA           MM    dP    ,V^MM.      MM   ,M9    MM    dP dM'      `MM     MM        MM    M YMb   M    MM   d    
   XV           MM"""bg.   ,M  `MM      MMmmdM9     MM"""bg. MM        MM     MM        MM    M  `MN. M    MMmmMM    
  AV    ,       MM    `Y   AbmmmqMA     MM  YM.     MM    `Y MM.      ,MP     MM        MM    M   `MM.M    MM   Y  , 
 AV    ,M       MM    ,9  A'     VML    MM   `Mb.   MM    ,9 `Mb.    ,dP'     MM        MM    M     YMM    MM     ,M 
AMMMMMMMF     .JMMmmmd9 .AMA.   .AMMA..JMML. .JMM..JMMmmmd9    `"bmmd"'     .JMML.    .JMML..JML.    YM  .JMMmmmmMMM 
                                                                                                                     
                                                                                                                     ''')
print(f" \n{Fore.BLUE}{Style.BRIGHT}DEMO VERSION{Style.RESET_ALL}\n \n\nTwitter: @thebarbotine\nDiscord: https://discord.gg/zZpvyz8brn\n")
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
if mode!='fake-money':
    real_balance=0
    for ex_str in ex_list.split(','):
        bal = ex[ex_str].fetchBalance()
        real_balance+=float(bal[symbol.split('/')[1]]['total'])
    with open(f"real_balance.txt","w") as f:
        f.write(str(real_balance))
else:
    with open(f"real_balance.txt","w") as f:
        f.write(str(balance))

while True:
    with open(f"real_balance.txt","r") as f:
        balance = str(f.read())
    if i>=1 and p.returncode==1:
        sys.exit(1)
    if mode == "fake-money":
        p=subprocess.run([python_command,"bot-fake-money.py",symbol,balance,renew,symbol,ex_list])
    elif mode == "real":
        p=subprocess.run([python_command,"bot.py",symbol,balance,renew,symbol,ex_list])
    else:
        printerror(m=f"mode input is incorrect.")
        sys.exit(1)
    i+=1
