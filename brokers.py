r"""
Python functions for crypto-brokers API
"""

__author__ = 'Hugo Demenez <hdemenez@hotmail.fr>'

import time,json,hmac,hashlib,requests,krakenex
from urllib.parse import urljoin, urlencode


class binance():
    '''API development for trade automation in binance markets'''
    def __init__(self):
        self.API_SECRET=''
        self.API_KEY=''

    def get_server_time(self):
        '''Function to get server time'''
        response = requests.get('https://api.binance.com/api/v3/time',params={}).json()
        try:
            return(response['serverTime'])
        except:
            return('unable to get server time')
     
    def get_klines_data(self,symbol):
        '''Function to get information from candles of 1minute interval [Open time,Open,High,Low,Close,Volume,Close time,
        Quote asset volume,Number of trades,Taker buy base asset volume,Taker buy quote asset volume,Ignore.]
        '''
        response = requests.get('https://api.binance.com/api/v3/klines',params={'symbol':symbol,'interval':'1m'}).json()
        return response

    def get_24h_stats(self,symbol):
        '''Function to get statistics for the last 24h'''
        response = requests.get('https://api.binance.com/api/v3/ticker/24hr',params={'symbol':symbol}).json()
        try:
            stats={
                'volume':response['volume'],
                'open':response['openPrice'],
                'high':response['highPrice'],
                'low':response['lowPrice'],
                'last':response['lastPrice'],
            }
        except:
            stats={
                'error':response,
            }
        finally:
            return stats
        
    def connect_key(self,path):
        '''Function to connect the api to the account'''
        try:
            with open(path, 'r') as f:
                self.API_KEY = f.readline().strip()
                self.API_SECRET = f.readline().strip()
            return ("Successfuly connected your keys")
        except:
            return ("Unable to read .key file")
        
    def price(self,symbol):
        '''Function to get symbol prices'''
        response = requests.get('https://api.binance.com/api/v3/ticker/bookTicker',params={'symbol':symbol}).json()
        try:
            bid=float(response['bidPrice'])
            ask=float(response['askPrice'])
            price={'bid':bid,'ask':ask}
        except:
            return response['msg']
        return price

    def account_information(self):
        '''Function to get account information'''
        timestamp = self.get_server_time()
        recvWindow=10000
        params = {
            'timestamp': timestamp,
            'recvWindow':recvWindow,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/account')
        response = requests.get(url, headers=headers, params=params).json()
        return response

    def get_balances(self):
        '''Function to get account balances'''
        try:
            balances=self.account_information()['balances']
        except:
            balances={'error':'unable to get balances'}
        return balances

    def get_open_orders(self):
        '''Function to get open orders'''
        timestamp = self.get_server_time()
        params = {
            'timestamp': timestamp,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/openOrderList')
        response = requests.get(url, headers=headers, params=params).json()
        try:
            code = response['code']
            return ('Unable to get orders')
        except:
            if response==[]:
                return {}
        finally:
            return response

    def create_limit_order(self,symbol,side,price,quantity):
        '''Function to create a limit order'''
        timestamp = int(time.time() * 1000)
        recvWindow=10000
        params = {
            'symbol':symbol,
            'side':side,
            'type':'LIMIT',
            'timeInForce':'GTC',
            'quantity':round(quantity,6),
            'price':price,
            'timestamp': timestamp,
            'recvWindow':recvWindow,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/order')
        response = requests.post(url, headers=headers, params=params).text
        return response

    def create_market_order(self,symbol,side,quantity):
        '''Function to create market order'''
        timestamp = int(time.time() * 1000)
        recvWindow=10000
        params = {
            'symbol':symbol,
            'side':side,
            'type':'MARKET',
            'quantity':round(quantity,6),
            'timestamp': timestamp,
            'recvWindow':recvWindow,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/order')
        response = requests.post(url, headers=headers, params=params).text
        return response

    def create_stop_loss_order(self,symbol,quantity,stopPrice,side):
        '''Function to create a stop loss'''
        timestamp = int(time.time() * 1000)
        recvWindow=10000
        params = {
            'symbol':symbol,
            'side':side,
            'type':'STOP_LOSS',
            'timeInForce':'GTC',
            'quantity':round(quantity,6),
            'price':stopPrice,
            'timestamp': timestamp,
            'recvWindow':recvWindow,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/order')
        response = requests.post(url, headers=headers, params=params).text
        return response

    def create_take_profit_order(self,symbol,quantity,profitPrice,side):
        '''Function to create a takeprofit'''
        timestamp = int(time.time() * 1000)
        recvWindow=10000
        params = {
            'symbol':symbol,
            'side':side,
            'type':'TAKE_PROFIT',
            'timeInForce':'GTC',
            'quantity':round(quantity,6),
            'price':profitPrice,
            'timestamp': timestamp,
            'recvWindow':recvWindow,
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {'X-MBX-APIKEY': self.API_KEY}
        url = urljoin('https://api.binance.com','/api/v3/order')
        response = requests.post(url, headers=headers, params=params).text
        return response

         
   
class kraken():
    '''API development for trading automation in kraken markets with krakenex'''
    def __init__(self):
        self.api=krakenex.API()
 
    def get_server_time(self):
        '''Function to get server time'''
        response = requests.get('https://api.kraken.com/0/public/Time',params={}).json()
        try:
            return(response['result']['unixtime'])
        except:
            return('unable to get server time')

    def get_24h_stats(self,symbol):
        '''Function to get statistics for the last 24h'''
        response = requests.get('https://api.kraken.com/0/public/Ticker',params={'pair':symbol}).json()
        
        try:
            for symbol in response['result']:
                stats={
                    'volume':response['result'][symbol]['v'][1],
                    'open':response['result'][symbol]['o'],
                    'high':response['result'][symbol]['h'][1],
                    'low':response['result'][symbol]['l'][1],
                    'last':response['result'][symbol]['c'][0],
                }
        except:
            stats={
                'error':response,
            }
        finally:
            return stats

    def get_klines_data(self,symbol,interval,timeframe):
        '''Function to get information from candles of 1minute interval
        <time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>
        since (1hour for minutes or 1week for days)
        max timeframe is 12hours for minute interval 
        max timeframe is 100 weeks for day interval
        '''
        if interval=='day':
            interval='1440'
            since_time=604800*timeframe
        elif interval=='hour':
            interval='60'
            since_time=86400*timeframe
        elif interval=='minute':
            interval='1'
            since_time=3600*timeframe
        else:
            return ('wrong interval')
        response = requests.get('https://api.kraken.com/0/public/OHLC',params={'pair':symbol,'interval':interval,'since':str(time.time()-since_time)}).json()
        try :
            for pair in response['result']:
                if pair=='last':
                    pair=pair1
                pair1=pair
            reponse = response['result'][pair]
            formated_response=[]
            for info in reponse:
                data={}
                data['time']=info[0]
                data['open']=info[1]
                data['high']=info[2]
                data['low']=info[3]
                data['close']=info[4]
                data['vwap']=info[5]
                data['volume']=info[6]
                data['count']=info[7]
                formated_response.append(data)
        except:
            formated_response = response['error']
        return formated_response

    def connect_key(self,path):
        '''Function to connect the api to the account'''
        self.api.load_key(path=path)

    def price(self,symbol):
        '''Function to get symbol prices'''
        response = requests.get('https://api.kraken.com/0/public/Ticker',params={'pair':symbol}).json()
        
        try:
            for name in response['result']:
                bid=float(response['result'][name]['b'][0])
                ask=float(response['result'][name]['a'][0])
                price={'bid':bid,'ask':ask}
        except:
            return response['error']
        return price

    def account_information(self):
        '''Function to get account information'''
        try:
            informations = self.api.query_private(method="Balance")['result']
        except:
            informations={'error':'unable to get informations'}
        return informations

    def get_balances(self):
        '''Function to get account balances'''
        try:
            balances = self.api.query_private(method="Balance")['result']
        except:
            balances={'error':'unable to get balances'}
        return balances

    def get_open_orders(self):
        '''Function to get open orders'''
        try:
            open_orders= self.api.query_private(method='OpenOrders')
            open_orders=open_orders['result']['open']
        except:
            return ('unable to get open orders')
        return open_orders

    def create_limit_order(self,symbol,side,price,quantity):
        '''Function to create a limit order'''
        data={
            'pair':symbol,
            'ordertype':'limit',
            'type':side,
            'volume':quantity,
            'price':price,
        }
        #On essaie de transmettre l'ordre au marché
        try :
            ordre = self.api.query_private(method='AddOrder',data=data)
        except:
            return ('unable to join market')
        return ordre

    def create_market_order(self,symbol,side,quantity):
        '''Function to create market order'''
        data={
            'pair':symbol,
            'ordertype':'market',
            'type':side,
            'volume':quantity,
        }
        #On essaie de transmettre l'ordre au marché
        try :
            ordre = self.api.query_private(method='AddOrder',data=data)
        except:
            return ('unable to join market')
        return ordre

    def create_stop_loss_order(self,symbol,quantity,stopPrice,side):
        '''Function to create a stop loss'''
        data={
            'pair':symbol,
            'ordertype':'stop-loss',
            'type':side,
            'volume':quantity,
            'price':stopPrice,
        }
        #On essaie de transmettre l'ordre au marché
        try :
            ordre = self.api.query_private(method='AddOrder',data=data)
        except:
            return ('unable to join market')
        return ordre

    def create_take_profit_order(self,symbol,quantity,profitPrice,side):
        '''Function to create a takeprofit'''
        data={
            'pair':symbol,
            'ordertype':'take-profit',
            'type':side,
            'volume':quantity,
            'price':profitPrice,
        }
        #On essaie de transmettre l'ordre au marché
        try :
            ordre = self.api.query_private(method='AddOrder',data=data)
        except:
            return ('unable to join market')
        return ordre



if __name__=='__main__':
    pass
