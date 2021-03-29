"""
This script's purpose is to collect data, over a specific time frame. In order to generate trading signals. 
We are going to use the brokers.py api to collect the prices depending on the broker name
"""

_autor__ = "Hugo Demenez"

import time,importlib,brokers

def data_harvest(broker_name,timeframe):
    start_time = time.time()
    end_time = start_time + timeframe
    broker = getattr(importlib.import_module('brokers'), '%s'%broker_name)
    
    while start_time!= end_time:
        print(brokers.kraken().get_klines_data(symbol="BTCEUR",interval="1"))
        start_time+=1
        




if __name__ == "__main__":
    data_harvest("binance",14)