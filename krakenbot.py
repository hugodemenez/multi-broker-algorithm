import krakenex,time,datetime,math
from trading_signal import buy_signal
#On definie l'api pour communiquer avec le serveur KRAKEN
kraken = krakenex.API()
kraken.load_key('kraken.key')
rendement=1.010


class Timeout():
    '''Definition de la classe pour avoir des informations en cas de perte de connexion'''
    def __init__(self):
        self.buy=0.0
        self.sell=0.0
        self.crypto=0.0
        self.stable=0.0

#On definit une variable Timeout qui va enregistrer les données essentielles
Timeout=Timeout()

class Position():
    '''Definition de la classe pour la position afin d'avoir ses informations apres le passage des ordres'''
    def __init__(self):
        self.price=0.0
        self.status='close'
        self.volume=0.0
        self.id=''
        self.level=1

#On definit la variable position qui va nous donner les infromations nécessaires pour la suite
Position=Position()

class Balance():
    '''Recuperation des informations du compte concernant les portefeuilles'''
    def __init__(self):
        '''Sachant que toutes les informations issues de KrakenAPI sont des dataframes, on doit les convertir en dictionnaires'''
        try :
            balance = kraken.query_private(method='Balance')['result']
            self.crypto = float(balance['XXBT'])
            self.stable = float(balance['ZEUR'])
            Timeout.crypto = float(balance['XXBT'])
            Timeout.stable = float(balance['ZEUR'])
        except:
            #Si jamais on n'arrive pas à collecter les informations alors on recupere la derniere info connue
            self.crypto=Timeout.crypto
            self.stable=Timeout.stable

class Price():
    '''Recupération des informations du marché sur Kraken'''
    def __init__(self):
        '''On sait que la premiere info de la liste est la demande et la deuxieme est l'offre, donc 1: prix de vente et 2: prix d'achat'''
        '''Attention on ne peut faire qu'une requete par seconde'''
        try:
            order_book = kraken.query_public(method='Ticker',data={'pair':'XXBTZEUR'})['result']['XXBTZEUR']
            self.buy = float(order_book['a'][0])
            self.sell = float(order_book['b'][0])
            Timeout.buy = float(order_book['a'][0])
            Timeout.sell = float(order_book['b'][0])
        except:
            #Si on n'arrive pas à collecter les info alors on prend la derniere connue
            self.buy = Timeout.buy
            self.sell= Timeout.sell



def open_position():
    '''Passage d'ordre au marché avec stop loss à 2-rendement''' 
    price = Price().buy
    '''On ouvre la position avec un stop loss prédéfinie'''
    data={
        'pair':'XXBTZEUR',
        'ordertype':'market',
        'type':'buy',
        'volume':str(Balance().stable*0.95/price),
        'close[ordertype]': 'stop-loss',
        'close[price]':Price().sell*(2-rendement),
    }
    #On essaie de transmettre l'ordre au marché
    try :
        ordre = kraken.query_private(method='AddOrder',data=data)
    except:
        print('unable to join market')
        return 

    #Si notre ordre renvoit une erreur alors on ne considere pas la position comme ouvert
    if ordre['error']!=[]:
        print(ordre)
        return 
    
    #On enregistre l'id de l'ordre pour pouvoir collecter les infos meme en cas de pépin
    try:
        save=open('id.txt','w')
        save.write(ordre['result']['txid'][0])
        save.close
    except:
        print('unable to save order')
        return 

    Position.status='open'    
    Position.level=1
    print(ordre)
    return 

def get_position_status():
    '''Verifie la situation de la position et deplace le stop loss si nécessaire'''
    ordre_status = kraken.query_private(method='OpenOrders')['result']['open']
    if ordre_status=={}:
        Position.status='close'
        return 
    else:
        #On regarde l'id de la position ouverte
        try:
            save=open('id.txt','r')
            Position.id=save.readline()
            save.close()
        except:
            print('there is no position id saved')
            return

        #On demande au serveur les informations de la position
        try:
            position_info = kraken.query_private(method='QueryOrders',data={'txid':Position.id})
            Position.price = float(position_info['result'][Position.id]['price'])
            Position.volume=float(position_info['result'][Position.id]['vol'])
        except:
            print('unable to get position data')
            return

        #On change le stop loss à condition que le prix actuel se trouve sous les 0.1% puis 0.2% etc...
        if Position.price*math.pow((rendement-1)/20+1,Position.level)<Price().sell:
            for stop_loss_id in ordre_status:
                txid = stop_loss_id
            try:
                kraken.query_private(method='CancelOrder',data={'txid':txid})
            except:
                print('unable to cancel stoploss')
                return
            #On replace un stoploss de plus en plus pres du prix actuel du marché
            data={
                'pair':'XXBTZEUR',
                'ordertype':'stop-loss',
                'type':'sell',
                'volume':Position.volume,
                'price':round(Price().sell*(1-(rendement-math.pow((rendement-1)/20+1,Position.level))),1),
            }
            #On essaie de transmettre l'ordre au marché
            try :
                print(kraken.query_private(method='AddOrder',data=data))
                Position.status='open'
                Position.level+=1
            except:
                print('unable to place a new stop loss')
                return 
        return

def main():
    '''Fonction principale (cerveau du programme)'''
    #On initialise le temps de fonctionnement du programme
    start_time = time.time()
    print('Starting Trading:')
    up_time=0
    while(True):
        try:
            get_position_status()
            #Si l'analyse donne un signal alors on place la position
            if buy_signal()=='buy' and Position.status=='close':
                open_position()
            #On ralenti le programme pour ne pas avoir trop de requetes vers les serveurs (risque d'etre deconnecté)
            time.sleep(1)
            up_time+=1
            if up_time%60==0:
                #On donne des informations sur la durée de fonctionnement et la situation des positions
                if up_time%3600==0:
                    print('Le programme fonctionne depuis %s'%str(datetime.timedelta(seconds=round(time.time(),0)-round(start_time,0))))
                    print('La position actuelle est %s'%Position.status)
                    #On redemarre le compteur pour ne pas risquer d'avoir une erreur si le temps est trop elevé.
                    up_time=0
        #Si on essaie de fermer le programme avec une combinaison clavier
        except KeyboardInterrupt:
            break

if __name__=='__main__':
    print(buy_signal())