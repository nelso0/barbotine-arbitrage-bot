balance=$3
echo $3 >| balance.txt
printf "\ec"
printf "                  ▄▀▀█▄▄    ▄▀▀█▄   ▄▀▀▀▀▄ 
                 ▐ ▄▀   █  ▐ ▄▀ ▀▄ █ █   ▐ 
                   █▄▄▄▀     █▄▄▄█    ▀▄   
                   █   █    ▄▀   █ ▀▄   █  
                  ▄▀▄▄▄▀ ▄ █   ▄▀ ▄ █▀▀▀   
                 █    ▐    ▐   ▐    ▐      
                 ▐                         \n"
printf "\nBarbotine Arbitrage System, by Nils Spenlehauer.\nUsage is strictly restricted to personal-use only under the CC BY-NC-SA 4.0 license. (https://creativecommons.org/licenses/by-nc-sa/4.0/)\n \nTwitter: @nelsodot\nDiscord: nelso#1800\nInstagram: @nelsorex\nGithub: nelso0\n \n"
while [[ 1 == 1 ]]; do
    if [[ "$1" == "classic" ]]; then
        if [[ -z $4 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $2 minutes period and $balance USDT."
            python3 bot-classic.py $symbol $balance $2 $symbol || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $4 with $2 minutes period and $balance USDT."
            python3 bot-classic.py $4 $balance $2 $4 || exit 1
            balance=`cat balance.txt`
        fi
    fi
    if [[ "$1" == "delta-neutral" ]]; then
        if [[ -z $4 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $2 minutes period and $balance USDT."
            python3 bot-delta-neutral.py $symbol $balance $2 $symbol || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $4 with $2 minutes period and $balance USDT."
            python3 bot-delta-neutral.py $4 $balance $2 $4 || exit 1
            balance=`cat balance.txt`
        fi
    fi
    if [[ "$1" == "fake-money" ]]; then
        if [[ -z $4 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            echo "[$(date)] Lauching Barbitrage on $symbol with $2 minutes period and $balance USDT."
            python3 bot-fake-money.py $symbol $balance $2 $symbol || exit 1
            balance=`cat balance.txt`
        else
            echo "[$(date)] Lauching Barbitrage on $4 with $2 minutes period and $balance USDT."
            python3 bot-fake-money.py $4 $balance $2 $4 || exit 1
            balance=`cat balance.txt`
        fi
    fi
done