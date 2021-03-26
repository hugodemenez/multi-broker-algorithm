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