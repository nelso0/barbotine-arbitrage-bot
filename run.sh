printf "\ec"
printf "██████╗   █████╗  ██████╗  ██████╗   ██████╗  ████████╗ ██╗ ███╗   ██╗ ███████╗
██╔══██╗ ██╔══██╗ ██╔══██╗ ██╔══██╗ ██╔═══██╗ ╚══██╔══╝ ██║ ████╗  ██║ ██╔════╝
██████╔╝ ███████║ ██████╔╝ ██████╔╝ ██║   ██║    ██║    ██║ ██╔██╗ ██║ █████╗  
██╔══██╗ ██╔══██║ ██╔══██╗ ██╔══██╗ ██║   ██║    ██║    ██║ ██║╚██╗██║ ██╔══╝  
██████╔╝ ██║  ██║ ██║  ██║ ██████╔╝ ╚██████╔╝    ██║    ██║ ██║ ╚████║ ███████╗
╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝   ╚═════╝     ╚═╝    ╚═╝ ╚═╝  ╚═══╝ ╚══════╝
                                                                       \n"
printf "\nBarbotine Arbitrage System, by nelso.\nUsage is strictly restricted to personal-use only under the CC BY-NC-SA 4.0 license. (https://creativecommons.org/licenses/by-nc-sa/4.0/)\n \nDiscord: nelso#1800\nGithub: nelso0\n \n"

read -p '[*] Exchange 1: ' ex1
read -p '[*] Exchange 2: ' ex2
read -p '[*] Exchange 3: ' ex3
read -p '[*] Total USDT investment: ' usdt_investment
read -p '[*] Symbol (put nothing if not): ' symbol
read -p '[*] Symbol renew time: ' symbol_renew

bash main.sh fake-money $symbol_renew $usdt_investment $ex1 $ex2 $ex3 $symbol


