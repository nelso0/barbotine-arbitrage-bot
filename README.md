## Σ Barbotine Arbitrage
<p align="left">
  <img alt="Barbotine arbitrage bot Logo" height="auto" src="https://i.ibb.co/cgdP6rL/Capture-d-e-cran-2024-07-28-a-15-39-40.png">
  <img alt="Barbotine arbitrage bot Logo" height="auto" src="https://i.ibb.co/wSmHNm8/image.png">
</p>

[![GitHub @nelso0](https://img.shields.io/github/followers/nelso0?label=follow&style=social)](https://github.com/nelso0)

## Table of content
* [Features](#features)
* [Demo video](#demo)
* [Prerequisites](#prerequis)
* [Installation](#installation)
* [Usage](#usage)
* [Links](#full-version)

<a name="features"/>
 
## Features

* Compatible with all [ccxt](https://github.com/ccxt/ccxt) exchanges
* Ready-to-run
* Precise at the orderbook level (close to a market-making algorithm)
* Can work with an unlimited number of exchanges at the same time
* Does a balance simulation for every possible opportunity to always choose the most profitable one
* Opportunities updates on Telegram and webhooks
* Full logging system

<a name="demo"/>
 
## Demo

demo video: https://youtu.be/Uw6ajbODid0

<a name="prerequis"/>
 
## Prerequisites

* Python 3+ inferior to 3.12! (for windows users: if python or pip isn't recognized as a command, make sure you have installed python by checking the box "add to PATH")

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
python run.py <mode> [renew-time-minutes] <balance-usdt-to-use> <pair> <exchanges list separated by commas (no space!)>
```


* ```<mode>``` = the mode you wanna use between ```fake-money``` and ```real```. See #full-version for real mode. 
  
  * ```fake-money``` will run the bot with the balance-usdt-to-use you put, with a virtual balance, just to test.
  * ```real``` will run the bot with real money.
  
* ```[renew-time-minutes]``` = ONLY IF YOU ENABLED RENEWAL SETTING IN THE CONFIG. If you enabled it, you have to put the number of minutes a session should last. After each session, the bot sells all the assets back to rebalance. Note: you can trigger a manual rebalance while in a session by pressing the Enter key.

* ```<balance-usdt-to-use>``` = how to be clearer? 

* ```<pair>``` = The pair you wanna arbitrage on.

* ```<exchanges list>``` = the exchanges you want the bot to scan the orderbooks on, among all the [CCXT-compatible exchanges](https://github.com/ccxt/ccxt). From a 2 exchanges minimum, up to an unlimited number. Don't forget to configure the exchanges in [exchange_config.py](exchange_config.py).

Note: as the bot needs to buy assets before getting started (it's necessary in order to operate without transfer between exchanges), if the pair you have chosen looses in value, you'll end up losing money when rebalancing. To avoid that, I created a delta-neutral feature that places a short order to "hedge" and counterbalance the purchase of coins by the bot. You can enable this feature in [exchange_config.py](exchange_config.py).

Examples:

with renewal disabled (default):
```sh
python run.py fake-money 500 EOS/USDT binance,okx,kucoin    # run the bot with 500 USDT and rebalance every 15 minutes, with binance okx and kucoin
```
with renewal enabled:
```sh
python run.py real 15 1000 SOL/USDT binance,poloniex,kucoin   # run the bot with 1000 USDT on binance phemex and bybit on SOL/USDT, and rebalance every 15 minutes.
```

<a name="full-version"/>

## Join the community

Community: [barbotine.xyz/discord](https://barbotine.xyz/discord)
Website: [barbotine.xyz](https://barbotine.xyz)
