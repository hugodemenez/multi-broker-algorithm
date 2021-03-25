import time,datetime,math,trading_signal,importlib,brokers

def broker_selection():
    '''Returns name of the selected broker
    
    '''
    broker_list=['kraken','binance']
    broker =''
    while broker not in broker_list:
        broker =str(input("Choose your broker:%s : "%broker_list))
    return broker


broker='kraken'
if broker =='kraken':
    broker=brokers.kraken()
if broker=='binance':
    broker=brokers.binance()
print(broker.price('ETHEUR'))

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



def open_position():
    '''Passage d'ordre au marché avec stop loss à 2-rendement'''
    '''On ouvre la position avec un stop loss prédéfinie''' 

    Position.status='open'    
    Position.level=1
    return 

def get_position_status():
    '''Verifie la situation de la position et deplace le stop loss avec un calcul pour le rapprocher au plus pres de la position en cas de hausse
    car la position se ferme sur le stop loss dans tous les cas
    '''


def main():
    '''Fonction principale (cerveau du programme)'''
    #On initialise le temps de fonctionnement du programme
    start_time = time.time()
    print('Starting Trading:')
    up_time=0
    while(True):
        try:
            #Verifie la situation de la position et deplace le stop loss si nécessaire (en supprimant le precedent)
            get_position_status()
            if Position.status=='close':
                #On actualise la librairie d'analyse afin de pouvoir changer la methode sans redémarrer le programme.
                try:
                    importlib.reload(trading_signal)
                    signal = trading_signal.buy_signal()
                except:
                    signal ='sell'
                    print('unable to get signal')
                #Si l'analyse donne un signal alors on place la position
                if signal=='buy':
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
    main()