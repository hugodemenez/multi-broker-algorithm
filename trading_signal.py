from tradingview_ta import TA_Handler, Interval


def buy_signal():
    '''Cette fonction est une fonction qui permet d'obtenir des signaux d'entrée par rapport à des analyses techniques'''
    #On paramètre la lecture des analyses qui sont fournies par TradingView
    handler  = TA_Handler()
    handler.set_symbol_as('BTCEUR')
    handler.set_exchange_as_crypto_or_stock('COINBASE')
    handler.set_screener_as_crypto()
    #On choisi de regarder le marché sur 1 minute
    handler.set_interval_as(Interval.INTERVAL_1_MINUTE)
    #On recupere les données des analyses techniques et du marché
    try:
        analyse=handler.get_analysis()
    except:
        print('Analyse du signal impossible')
        #Si l'analyse echoue alors on considere que l'on a pas eu de signal d'entrée
        return 'sell'
    #Méthode : On regarde le RSI, si il est en oversold, on regarde l'EMA 200 si on s'ecarte à plus de 0.4% et on utilise les resistances.
    #pour reduire les entrées aux meilleurs moments possibles

    current_price=Price().buy
    RSI=analyse.indicators['RSI']
    EMA_200=analyse.indicators['EMA200']
    resistances=analyse_resistances()

    #Si on se situe au niveau des resistances
    if RSI<30 and current_price<EMA_200*0.996:
        for resistance in resistances:
            if current_price<(float(resistance)*1.001) and current_price>(float(resistance)):
                return 'buy'

    else:
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
    pass