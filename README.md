<h1 align="center">EasyTrading</h1>


<div align="center">
  <strong>Automate your trades on many brokers with python</strong>
</div>


<br />





<div align="center">
  <sub>Built by
  <a href="https://github.com/hugodemenez">Hugo Demenez</a> and
  <a href="https://github.com/hugodemenez/EasyTrading/graphs/contributors">
    contributors
  </a>
</div>

## Table of Contents
- [Features](#features)
- [Example](#example)
- [Philosophy](#philosophy)
- [Events](#events)
- [State](#state)
- [Routing](#routing)
- [Server Rendering](#server-rendering)
- [Components](#components)
- [Optimizations](#optimizations)
- [FAQ](#faq)
- [API](#api)
- [Installation](#installation)
- [See Also](#see-also)
- [Support](#support)

## Features
- __Get Price data for symbol:__ 
- __Get account information:__ 
- __Get open orders:__ 
- __Place orders:__ 


## Example
```python3

import brokers

broker=brokers.binance()

#Public data
print(
    broker.price(),
    broker.get_klines_data(),
    broker.get_24h_stats(),
    )

#To connect api
print(
    broker.connect_key("binance.key")
)

#Private data
print(
    broker.account_information(),
    broker.get_open_orders(),
    broker.get_balances(),
    broker.create_market_order(symbol='BTCUSD',side='buy',quantity=1),
    broker.create_limit_order(symbol='BTCUSD',side='buy',quantity=1,price=10000),
    broker.create_take_profit_order(symbol='BTCUSD',side='buy',quantity=1,profitPrice=100000),
    broker.create_stop_loss_order(symbol='BTCUSD',side='buy',quantity=1,stopPrice=1000),
)

```


## Philosophy
I believe trading should be as simple as buying potatoes,
that's why I tried my best to make everything clearer.
Who doesn't want to win the market while sleeping ?



## Optimizations
I will try my best to deal with every exceptions. And to make a user-friendly gui as minimal as possible.

## Installation

<a href="https://github.com/hugodemenez/EasyTrading/archive/refs/heads/main.zip" target="_blank"><img src="https://github.com/hugodemenez/EasyTrading/blob/main/assets/download.gif"></a>

```
python3 brain.py
```


## License
[MIT](https://tldrlegal.com/license/mit-license)

