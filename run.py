import subprocess
from exchange_config import *
import sys, os
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
import time
from os import name,system
from colorama import Style, Fore, init
init()
def clear():
    if name == 'nt':
      system('cls')
    else:
        system('clear')

try:
    if len(sys.argv) < 3:
        input_list = ["mode (fake-money or real)", "renewal period (in minutes)", "balance to use", "symbol", "exchanges list separated without space with commas (,)"]
        if not renewal:
            input_list.remove("renewal period (in minutes)")
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

        if mode!='fake-money':
            real_balance=0
            for ex_str in ex_list.split(','):
                bal = ex[ex_str].fetchBalance()
                real_balance+=float(bal[symbol.split('/')[1]]['total'])
            with open(f"real_balance.txt","w") as f:
                f.write(str(real_balance))

        if renewal:
            subprocess.run([how_do_you_usually_launch_python,f"main.py",mode,renew_time,balance,symbol,ex_list])
        else:
            subprocess.run([how_do_you_usually_launch_python,f"main.py",mode,balance,symbol,ex_list])

    else:
        if (len(sys.argv) != 6) and renewal:
            printerror(m=f"Not correctly configured. Usage:\n \n{how_do_you_usually_launch_python} run.py <mode> <renewal period minutes> <balance to use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        if (len(sys.argv) != 5) and not renewal:
            printerror(m=f"Not correctly configured. Usage:\n \n{how_do_you_usually_launch_python} run.py <mode> <balance to use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
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
        i=0

        while True:
            with open(f"real_balance.txt","r") as f:
                balance = float(f.read())
            if i>=1 and p.returncode==1:
                sys.exit(1)
            if mode == "fake-money":
                if os.path.exists('bot-fake-money.py'):
                    p=subprocess.run([how_do_you_usually_launch_python,"bot-fake-money.py",symbol,balance,renew_time,symbol,ex_list])
                else:
                    printerror(m=f'please put the file "bot-fake-money.py" in the current directory.')
            elif mode == "real":
                if os.path.exists('bot.py'):
                    p=subprocess.run([how_do_you_usually_launch_python,"bot.py",symbol,balance,renew_time,symbol,ex_list])
                else:
                    printerror(m=f'please put the file "bot.py" in the current directory.')
            else:
                printerror(m=f"mode input is incorrect.")
                sys.exit(1)
            i+=1
except KeyboardInterrupt:
    if mode!='fake-money':
        print(" \n \n \n")
        clear()
        answered = False
        while answered == False:
            inp = input(f"{get_time()} CTRL+C was pressed. Do you want to sell all crypto back? (y)es / (n)o\n \ninput: ")
            append_new_line('logs/logs.txt',f"{get_time_blank()} INFO: ctrl+c was pressed.")
            if inp.lower() == "y" or inp.lower() == "yes":
                answered = True
                emergency_convert_list(symbol,[ex_list.split(',')[i] for i in range(len(ex_list.split(',')))])
                sys.exit(1)
            if inp.lower() == "n" or inp.lower() == "no":
                answered = True
                sys.exit(1)
            else:
                answered = False
    else:
        pass

