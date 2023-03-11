balance=$3
renew=$2
echo $3 >| start_balance-$(echo $5 | tr -d '[:punct:]').txt
echo $3 >| balance-$(echo $5 | tr -d '[:punct:]').txt
printf "\ec"
printf "                  ▄▀▀█▄▄    ▄▀▀█▄   ▄▀▀▀▀▄ 
                 ▐ ▄▀   █  ▐ ▄▀ ▀▄ █ █   ▐ 
                   █▄▄▄▀     █▄▄▄█    ▀▄   
                   █   █    ▄▀   █ ▀▄   █  
                  ▄▀▄▄▄▀ ▄ █   ▄▀ ▄ █▀▀▀   
                 █    ▐    ▐   ▐    ▐      
                 ▐                         \n"
printf "\nBarbotine Arbitrage System, by nelso.\nUsage is strictly restricted to personal-use only under the CC BY-NC-SA 4.0 license. (https://creativecommons.org/licenses/by-nc-sa/4.0/)\n \nDiscord: nelso#1800\nGithub: nelso0\n \n"
while [[ 1 == 1 ]]; do
    if [[ "$1" == "classic" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-classic.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $7 with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-classic.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        fi
    fi
    if [[ "$1" == "delta-neutral" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-delta-neutral.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $7 with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-delta-neutral.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        fi
    fi
    if [[ "$1" == "fake-money" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-fake-money.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $7 with $renew minutes period and $balance USDT."
            echo "[$(date)] Exchanges choosed: $4 / $5 / $6"
            python3 bot-fake-money.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`cat balance.txt`
        fi
    fi
done