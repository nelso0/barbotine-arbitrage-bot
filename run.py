import subprocess
from exchange_config import *
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
import time
from os import path, name,system
from colorama import Style, Fore, init
init()
def clear():
    if name == 'nt':
      system('cls')
    else:
        system('clear')
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

try:
    if len(sys.argv) < 2:
        input_list = ["mode (fake-money, classic, delta-neutral)", "renew time (in minutes)", "balance to use", "symbol", "exchanges list separated without space with commas (,)"]
        if not renewal:
            input_list.remove("renew time (in minutes)")
        output = []
        
        for inputt in input_list:
            output.append(input(inputt+" >>> "))
        
        mode = output[0]
        if not renewal:
            renew_time = "525600"
            balance=output[1]
            symbol = output[2]
            ex_list = output[3]
        else:
            renew_time = output[1]
            balance=output[2]
            symbol = output[3]
            ex_list = output[4]

        with open(f"start_balance.txt","w") as f:
            f.write(balance)
            f.close()
        with open(f"balance.txt","w") as f:
            f.write(balance)
            f.close()

        if renewal:
            subprocess.run([how_do_you_usually_launch_python,f"main.py",mode,renew_time,balance,symbol,ex_list])
        else:
            subprocess.run([how_do_you_usually_launch_python,f"main.py",mode,balance,symbol,ex_list])

    else:
        if (len(sys.argv) < 6 or len(sys.argv) > 6) and renewal:
            print(f"Not correctly configured. Usage:\n \n{how_do_you_usually_launch_python} run.py <mode> <symbol-renew-time> <balance-to-use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        if (len(sys.argv) < 5 or len(sys.argv) > 5) and not renewal:
            print(f"Not correctly configured. Usage:\n \n{how_do_you_usually_launch_python} run.py <mode> <balance-to-use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        args = sys.argv
        
        mode = args[1]
        if not renewal:
            renew_time = "525600"
            balance=args[2]
            symbol = args[3]
            ex_list = args[4]
        else:
            renew_time = args[2]
            balance=args[3]
            symbol = args[4]
            ex_list = args[5]

        with open(f"start_balance.txt","w") as f:
            f.write(balance)
            f.close()
        with open(f"balance.txt","w") as f:
            f.write(balance)
            f.close()
        
        print('''
                                                                                                                     
                                                                                                                     
VMA""YMM      `7MM"""Yp,      db      `7MM"""Mq.  `7MM"""Yp,   .g8""8q.  MMP""MM""YMM `7MMF'`7MN.   `7MF'`7MM"""YMM  
 VMA  `7        MM    Yb     ;MM:       MM   `MM.   MM    Yb .dP'    `YM.P'   MM   `7   MM    MMN.    M    MM    `7  
  VMA           MM    dP    ,V^MM.      MM   ,M9    MM    dP dM'      `MM     MM        MM    M YMb   M    MM   d    
   XV           MM"""bg.   ,M  `MM      MMmmdM9     MM"""bg. MM        MM     MM        MM    M  `MN. M    MMmmMM    
  AV    ,       MM    `Y   AbmmmqMA     MM  YM.     MM    `Y MM.      ,MP     MM        MM    M   `MM.M    MM   Y  , 
 AV    ,M       MM    ,9  A'     VML    MM   `Mb.   MM    ,9 `Mb.    ,dP'     MM        MM    M     YMM    MM     ,M 
AMMMMMMMF     .JMMmmmd9 .AMA.   .AMMA..JMML. .JMM..JMMmmmd9    `"bmmd"'     .JMML.    .JMML..JML.    YM  .JMMmmmmMMM 
                                                                                                                     
                                                                                                                     ''')
        print(f" \n{Fore.BLUE}{Style.BRIGHT}DEMO VERSION{Style.RESET_ALL}\n \nnelsorex.eth\nTwitter: @nelsorex\nDiscord: nelsorex\n")
        i=0

        while True:
            if i>=1 and p.returncode==1:
                sys.exit(1)
            if mode == "fake-money":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-fake-money.py",symbol,balance,renew_time,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            elif mode == "classic":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-classic.py",symbol,balance,renew_time,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            elif mode == "delta-neutral":
                p=subprocess.run([how_do_you_usually_launch_python,"bot-delta-neutral.py",symbol,balance,renew_time,symbol,ex_list])
                with open(f"balance.txt") as f:
                    balance=f.read()
            else:
                print(f"Mode input is incorrect.")
                sys.exit(1)
            i+=1
except KeyboardInterrupt:
    if ctrl_c_handling and mode!='fake-money':
        print(" \n \n \n")
        clear()
        answered = False
        while answered == False:
            inp = input(f"{Style.DIM}{get_time()}{Style.RESET_ALL} CTRL+C was pressed. Do you want to sell all crypto back? (y)es / (n)o\n \ninput: ")
            if inp == "y" or inp == "Y" or inp == "yes" or inp == "Yes":
                answered = True
                emergency_convert_list(symbol,[ex_list.split(',')[i] for i in range(len(ex_list.split(',')))])
                sys.exit(1)
            if inp == "n" or inp == "N" or inp == "no" or inp == "No":
                answered = True
                sys.exit(1)
            else:
                answered = False
    else:
        pass

