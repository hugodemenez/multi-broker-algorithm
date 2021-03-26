r"""
Apres un grand nombre de recherches et de temps passé à analyser les marchés, il est sûr que la recette magique n'existe pas. Il faut la fabriquer.
Je pense qu'il est important de créer son propre outil d'analyse. Pour cela il est simplement nécessaire de recuperer les informations basiques comme
une moyenne mobile par exemple. Ou un volume. Ensuite on peut fabriquer des fonctions mathématiques avec cela.
Tradingview, nous permet de récuperer efficacement ce type d'information. Mais il ne faut pas aller plus loin, car on réussi sur le long terme seulement ce que l'on maîtrise.
"""

from tradingview_ta import TA_Handler, Interval
import brokers


valeurs={'analyse_1h':['SMA30','SMA10'],
    'analyse_15m':['SMA30','SMA10'],
    'analyse_1m':['SMA30','SMA10'],
}

print(brokers.binance().get_24h_stats(symbol='BTCEUR'))
print(brokers.kraken().get_24h_stats(symbol='BTCEUR'))
def buy_signal(symbol):
    '''Cette fonction est une fonction qui permet d'obtenir des signaux d'entrée par rapport à des analyses techniques'''
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

    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'

    
    
    return 'sell'


if __name__=="__main__":
    buy_signal()
    pass
