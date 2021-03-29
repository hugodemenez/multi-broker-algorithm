from tradingview_ta import TA_Handler, Interval



def buy_signal(symbol,broker_name):
    '''Cette fonction est une fonction qui permet d'obtenir des signaux d'entrée par rapport à des analyses techniques'''
    #Méthode : On regarde le RSI, s'il est en oversold, on regarde deux MACD un sur 1h et un sur 15min
    #pour reduire les entrées aux meilleurs moments possibles

    #On paramètre la lecture des analyses qui sont fournies par TradingView
    handler  = TA_Handler()
    handler.set_symbol_as(symbol)
    handler.set_exchange_as_crypto_or_stock(broker_name.upper())
    handler.set_screener_as_crypto()
    #On choisi de regarder le marché sur 1 heure
    handler.set_interval_as(Interval.INTERVAL_1_HOUR)
    #On recupere les données des analyses techniques et du marché
    try:
        analyse=handler.get_analysis()
        #On regarde le MACD sur 1h
        MACD_1H = analyse.indicators['MACD.macd']
        MACD_1H_signal = analyse.indicators['MACD.signal']
    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'
    
    #On choisi de regarder le marché sur 15 minutes
    handler.set_interval_as(Interval.INTERVAL_15_MINUTES)
    #On recupere les données des analyses techniques et du marché
    try:
        analyse=handler.get_analysis()
        #On regarde le MACD sur 15min
        MACD_15m = analyse.indicators['MACD.macd']
        MACD_15m_signal = analyse.indicators['MACD.signal']
    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'
    
    #On choisi de regarder le marché sur 1 minute
    handler.set_interval_as(Interval.INTERVAL_1_MINUTE)
    #On recupere les données des analyses techniques et du marché
    try:
        analyse=handler.get_analysis()

        RSI=analyse.indicators['RSI']
    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'
    
    #Si on se situe au niveau des resistances
    if RSI<=30 :
        if MACD_15m>MACD_15m_signal*0.95 and MACD_1H>MACD_1H_signal:
            return 'buy'
    return 'sell'

def analyse_resistances():
    '''Fonction pour recuperer le fichier texte avec les resistances'''
    resistances=[]
    with open("resistances.txt") as f:
        for line in f:
            line = str.strip(line)
            try:
                resistances.append(float(line))
            except:
                print('Probleme dans le fichier resistances')

    resistances.sort()
    resistances.remove(resistances[0])
    resistances.remove(resistances[len(resistances)-1])
    return resistances



if __name__=='__main__':
    print(buy_signal(symbol="BTCEUR",broker_name="binance"))
    pass