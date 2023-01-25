<p align="left">
  <img width="30%" height="30%" src="https://bas.teleporthq.app/playground_assets/bas-logo-rouge-600w.png">
</p>
<button data-shoppy-product="SNIB5Zf">Pay</button>
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/nelsodot.svg?style=social&label=%20%40nelsodot)](https://twitter.com/nelsodot)
[![GitHub @nelso0](https://img.shields.io/github/followers/nelso0?label=follow&style=social)](https://github.com/nelso0)

More than a simple algorithm, [Barbotine Arbitrage System (B.A.S)](https://bas.teleporthq.app) is a complete portfolio management system based on the price difference opportunities of the same asset on several centralized trading platforms.
To eliminate the risks and variables to be taken into account, B.A.S operates without any transfer of assets between trading platforms. It also operates in a delta-neutral situation, which brings it even closer to zero risk.

## Table of content
* [Features](#features)
* [Demo](#demo)
* [Prerequisites](#prerequis)
* [Installation](#installation)
* [Usage](#usage)
* [To do](#todo)
* [Real money (and profits)](#full-version)
* [Contact](#contact)
<a name="features"/>
 
## Features

* True trading fees support
* Zero-risk (no speculation)
* Full live tracking on Telegram and Discord webhooks
* Permanent live rate display in the terminal
* Compatible with all [ccxt](https://github.com/ccxt/ccxt) exchanges simultaneously (multi-threading).

<a name="demo"/>
 
## Demo

I created a Discord server where you can track live results of B.A.S with $10k starting balance on SOL/USDT
Join it [here](https://discord.gg/Y7MeEMGKnn)

![](https://cdn.discordapp.com/attachments/876447732259225612/1066353879568105512/demo.gif)

What an opportunity looks like (0 trading fees example):

![](https://media.discordapp.net/attachments/876447732259225612/1066487526807842836/demo_trades.gif)
In general, you can't know in advance how many opportunities there will be, and it's not constant at all. Plus, it also changes completely from one crypto to another. But I have observed that the more volatile the market is, the more opportunities there are. I'm still doing my research on this, you can help me if you want (contact info below)

<a name="prerequis"/>
 
## Prerequisites

The things you need before installing the software.

* Python 3.*
* Machine which can run bash scripts (best is macOS or Linux env.)
* (not mandatory) AWS, Google Cloud or any cloud computing service to run the system 24/7
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) package installed

<a name="installation"/>
 
## Installation

1. Clone the repository 
```sh
$ git clone https://github.com/nelso0/BAS.git
```
2. Go to the B.A.S repository you just cloned
```sh
$ cd BAS
```
3. Install all the requirements to run the arbitrage system
```sh
$ pip install -r requirements.txt
```
4. Put your 3 api keys, passwords etc (binance, okx, kucoin) and your telegram bot details in [exchange_config.py](exchange_config.py)

**Then you're ready to run B.A.S!**

<a name="usage"/>
 
## Usage

Usage: 

```sh
$ bash main.sh [mode] [symbol-renew-time-minutes] [balance-usdt-to-use] {symbol}
```

* ```[mode]``` = the mode you wanna use among bot-fake-money, bot-classic, bot-delta-neutral. 
  
  * ```fake-money``` will run the bot with the balance-usdt-to-use you put, to test without any actual money. You have access to this mode only, read [full version](#full-version).
  
* ```[symbol-renew-time-minutes]``` = the timeframe you wanna use to switch symbol. If you put 60, it will renew the symbol each hour. Note that the new symbol is automatically selected by the [best_symbol.py](best-symbol.py) script.

* ```[balance-usdt-to-use]``` = how to be clearer? 

* ```{symbol}``` = Not mandatory. If you put a symbol, it will run continuously on this symbol, and so you can put a big [symbol-renew-time-minutes].

Examples:

```sh
$ bash main.sh fake-money 15 1000    # run the system with 1000 USDT and renew symbol every 15 minutes.
```
```sh
$ bash main.sh classic 15 1000 SOL/USDT   # run the system with 1000 USDT on SOL/USDT continuously (change the symbol to SOL/USDT each 15 minutes).
```
```sh
$ bash main.sh delta-neutral 60 2000   # run the system in a delta-neutral situation with 2000 USDT and renew the symbol each hour. Note that with same amount of USDT, the delta-neutral mode will have 2/3 of the profits of the classic mode because it has less liquidity to invest in arbitrage opportunities. (Yes, a delta-neutral situation has a cost.)
```
<a name="todo"/>
 
## To do

- [x] Improve lisibility and UI
- [x] Add full trading fee support
- [X] Sometimes crypto balance can be slightly negative (fixed)

<a name="full-version"/>
 
## Full version

I also made a full version which operates with real money (and real profits!).
In general, the more volatile the crypto market, the more arbitrage opportunities there are - so the profits vary a lot from a month to another. 
I'd say that the ROI/month can go from **5% to 30%** easily. 

Reminder: you can check B.A.S running live [here](discord.gg/Y7MeEMGKnn).
 
You can also contact me if you have a question, or if you want to talk about B.A.S, how it works etc.

<a name="contact"/>
 
## Contact

Twitter: [@nelsodot](https://twitter.com/nelsodo)

Discord: nelso#1800

Email: [nils.spen@gmail.com](mailto:nils.spen@gmail.com)
