r"""
After a lot of researchs and time spent analyzing the markets, it is certain that the magic recipe does not exist. We have to build it.
I think it’s important to create your own analytical tools. For this it is simply necessary to retrieve basic information like
a moving average, for example. Or a volume. Then we can make mathematical functions out of that.
Tradingview_ta allows us to efficiently retrieve this type of information. But we must not go any further, because in the long term we only succeed in what we master.

don't hesitate to give a star to : https://github.com/deathlyface/python-tradingview-ta
"""

__author__ = 'Hugo Demenez <hdemenez@hotmail.fr>'

from tradingview_ta import TA_Handler, Interval
import brokers


def buy_signal(symbol):
    '''Cette fonction est une fonction qui permet d'obtenir des signaux d'entrée par rapport à des analyses techniques'''
    valeurs={'analyse_1h':['SMA30','SMA10'],
    'analyse_15m':['SMA30','SMA10'],
    'analyse_1m':['SMA30','SMA10'],
    }

    #On paramètre la lecture des analyses qui sont fournies par TradingView
    handler  = TA_Handler()
    handler.set_symbol_as(symbol)
    handler.set_exchange_as_crypto_or_stock('COINBASE')
    handler.set_screener_as_crypto()
    try:
        #On recupere les données des analyses techniques et du marché
        resultat={}
        #On choisi de regarder le marché sur 1 heure
        handler.set_interval_as(Interval.INTERVAL_1_HOUR)
        analyse_1h=handler.get_analysis()
        for outil in valeurs['analyse_1h']:
            resultat[outil+'_1h']=(analyse_1h.indicators[outil])
        #On choisi de regarder le marché sur 15 minutes
        handler.set_interval_as(Interval.INTERVAL_15_MINUTES)
        analyse_15m=handler.get_analysis()
        for outil in valeurs['analyse_15m']:
            resultat[outil+'_15m']=(analyse_15m.indicators[outil])
        handler.set_interval_as(Interval.INTERVAL_1_MINUTE)
        analyse_1m=handler.get_analysis()
        for outil in valeurs['analyse_1m']:
            resultat[outil+'_1m']=(analyse_1m.indicators[outil])
        print(resultat)
        print(brokers.binance().get_24h_stats(symbol))
    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'

    return 'sell'


if __name__=="__main__":
    
    buy_signal('ETHEUR')
    pass
