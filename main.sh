balance=$3
renew=$2
echo $3 >| start_balance-$(echo $7 | tr -d '[:punct:]').txt
echo $3 >| balance-$(echo $7 | tr -d '[:punct:]').txt
while [[ 1 == 1 ]]; do
    if [[ "$1" == "classic" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            python3 bot-classic.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`cat balance-$(echo $7 | tr -d '[:punct:]').txt`
        else
            python3 bot-classic.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`cat balance-$(echo $7 | tr -d '[:punct:]').txt`
        fi
    fi
    if [[ "$1" == "classic" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            python3 bot-classic.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`cat balance-$(echo $7 | tr -d '[:punct:]').txt`
        else
            python3 bot-classic.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`cat balance-$(echo $7 | tr -d '[:punct:]').txt`
        fi
    fi
    if [[ "$1" == "delta-neutral" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            python3 bot-delta-neutral.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`balance-$(echo $7 | tr -d '[:punct:]').txt`
        else
            python3 bot-delta-neutral.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`balance-$(echo $7 | tr -d '[:punct:]').txt`
        fi
    fi
    if [[ "$1" == "fake-money" ]]; then
        if [[ -z $7 ]]; then
            echo "[$(date)] Searching best symbol..."
            python3 best-symbol.py || exit 1
            symbol=`cat symbol.txt`
            echo "[$(date)] Found it! symbol: $symbol"
            python3 bot-fake-money.py $symbol $balance $renew $symbol $4 $5 $6 || exit 1
            balance=`balance-$(echo $7 | tr -d '[:punct:]').txt`
        else
            python3 bot-fake-money.py $7 $balance $renew $7 $4 $5 $6 || exit 1
            balance=`balance-$(echo $7 | tr -d '[:punct:]').txt`
        fi
    fi
done