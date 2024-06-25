<p align="left">
  <img alt="Barbotine arbitrage bot Logo" width="10%" height="auto" src="https://i.ibb.co/gy9mb2k/logo.png">
</p>

[![Twitter @nelsodot](https://img.shields.io/twitter/url/https/twitter.com/nelsorex.svg?style=social&label=%20%40nelsorex)](https://twitter.com/nelsorex)
[![GitHub @nelso0](https://img.shields.io/github/followers/nelso0?label=follow&style=social)](https://github.com/nelso0)

## Table of content
* [Features](#features)
* [Demo video](#demo)
* [Prerequisites](#prerequis)
* [Installation](#installation)
* [Usage](#usage)
* [Real version](#full-version)
* [Contact and full documentation](#contact)

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

Note: as the bot needs to buy assets before getting started (it's necessary in order to operate without transfer between exchanges, read more [here](https://medium.com/@barbotine/how-to-exploit-arbitrage-opportunities-using-python-in-centralized-exchanges-like-binance-or-kucoin-805b5bf7b2f2)), if the pair you have chosen looses in value, you'll end up losing money when rebalancing. To avoid that, I created a delta-neutral feature that places a short order to "hedge" and counterbalance the purchase of coins by the bot. You can enable this feature in [exchange_config.py](exchange_config.py).

Examples:

```sh
python run.py fake-money 15 500 EOS/USDT binance,okx,kucoin    # run the bot with 500 USDT and rebalance every 15 minutes, with binance okx and kucoin
```
```sh
python run.py real 15 1000 SOL/USDT binance,poloniex,kucoin   # run the bot with 1000 USDT on binance phemex and bybit on SOL/USDT, and rebalance every 15 minutes.
```

<a name="full-version"/>
 
## Real money modes

The source code of the arbitrage bot that works with real money is available for Barbotine Capital supporters.

More information: [barbotine.xyz/](https://barbotine.xyz/)

## Contact and documentation

[nelso@barbotine.xyz](mailto:nelso@barbotine.xyz)

[Full documentation](https://documentation.barbotine.xyz)
