from sys import path
import brokers
from configparser import ConfigParser


#On configure l'api
api = brokers.binance_api()
api.connect_key(path=r"C:\Users\Hugo\OneDrive\binance.key")

print(api.create_stop_loss_order(symbol='BTCEUR',quantity=0.002,stopPrice=api.price['ask'],side='buy'))