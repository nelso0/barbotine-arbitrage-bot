<p align="left">
  <img alt="Barbotine Arbitrage System Logo" width="30%" height="30%" src="https://cdn.discordapp.com/attachments/876447732259225612/1095369391052443708/bas.svg">
</p>

[![Twitter @nelsodot](https://img.shields.io/twitter/url/https/twitter.com/nelsorex.svg?style=social&label=%20%40nelsorex)](https://twitter.com/nelsorex)
[![GitHub @nelso0](https://img.shields.io/github/followers/nelso0?label=follow&style=social)](https://github.com/nelso0)

## Table of content
* [Features](#features)
* [Demo](#demo)
* [Prerequisites](#prerequis)
* [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)
* [Real version](#full-version)
<a name="features"/>
 
## Features

* Compatible with almost any exchange (all [ccxt](https://github.com/ccxt/ccxt) exchanges).
* Pre-calculates all future transactions fees to know the exact possible profit before all transactions
* Zero-risk (no speculation)
* Full live tracking on Telegram and Discord webhooks
* Permanent live rate display in the terminal

<a name="demo"/>
 
## Demo

Message from after the video: the nb_exchanges variable in the config is now deleted, the bot automatically detects the number of exchanges you put.

Here is the setup & demo video for beginners: https://youtu.be/Uw6ajbODid0

<a name="prerequis"/>
 
## Prerequisites

The things you need before installing the software.

* Python 3.9+ (for windows users: if python or pip isn't recognized as a command, make sure you have installed python by checking the box "add to PATH")
* Nothing else lol

<a name="installation"/>
 
## Installation

1. Clone the repository 
```sh
git clone https://github.com/nelso0/barbotine-arbitrage-bot # you can also download the zip file
```
2. Go to the repository you just cloned
```sh
cd barbotine-arbitrage-bot
```
3. Install all the requirements to run the arbitrage system
```sh
pip install -r requirements.txt
```
4. Set your configuration details in [exchange_config.py](exchange_config.py)
5. Run with:
```sh
python run.py
```

<a name="usage"/>
 
## Usage

You can also run it with one line like this:

```sh
python run.py <mode> [renew-time-minutes] <balance-usdt-to-use> <symbol> <exchanges list separated by commas (no space!)>
```


* ```<mode>``` = the mode you wanna use among ```fake-money```, ```classic```, and ```delta-neutral```. See #full-version for classic and delta-neutral modes. 
  
  * ```fake-money``` will run the bot with the balance-usdt-to-use you put, with a virtual balance, just to test.
  * ```classic``` will run the bot with real USDT.
  * ```delta-neutral```will run the bot with real USDT also, but in a delta-neutral situation. (a bit less profits but you won't loose a cent if the crypto you're using dump in 5 minutes (for very very careful people).
  
  
  
* ```[renew-time-minutes]``` = ONLY IF YOU ENABLED RENEWAL SETTING IN THE CONFIG. If you enabled it, you have to put the number of minutes a session should last. After each session, the bot sells all the assets back to USDT and start again. It's for volatile assets if you want to refresh the price at which the bot bought the asset.



* ```<balance-usdt-to-use>``` = how to be clearer? 



* ```<symbol>``` = The symbol you wanna arbitrage on. Every time it renews, it sells all the crypto and rebuy the crypto asset at the new price. 



* ```<exchanges list>``` = the exchanges you want to use among all the CCXT-compatible exchanges. At least 2 exchanges, theorically infinite maximum. Don't forget to configure the exchanges in [exchange_config.py](exchange_config.py).


Note: you can put a minimum profit in USD or % in [exchange_config.py](exchange_config.py). The bot will only take the trade if the profit is > (superior) to your value. You can also use pairs without USDT, like ETH/BTC.

Examples:

```sh
python run.py fake-money 15 500 EOS/USDT binance,okx,kucoin    # run the system with 500 USDT and renew the session every 15 minutes, with binance okx and kucoin
```
```sh
python run.py classic 15 1000 SOL/USDT binance,poloniex,kucoin   # run the system with 1000 USDT on binance phemex and bybit on SOL/USDT, and renew the session every 15 minutes.
```
```sh
python run.py delta-neutral 60 750 BTC/USDT okx,cryptocom,huobi   # run the system in a delta-neutral situation with 750 USDT and renew the session each hour, on okx crypto.com and huobi. Note that with same amount of USDT, the delta-neutral mode will have 2/3 of the profits of the classic mode because it has less liquidity to invest in arbitrage opportunities.
```

## Contact

[barbotine.capital](https://barbotine.capital)

<a name="full-version"/>
 
## Full version

There is also a full version which operates with real dollars.

Link: [barbotine.capital/arbitrage](https://barbotine.capital/arbitrage)

/!\ No financial advise, DYOR /!\
