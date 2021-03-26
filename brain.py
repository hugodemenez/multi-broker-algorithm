"""
This program is the first version of a trading bot,
It is made simple to use, the only things you have to do is to create your .key and place it in C:\\
You can simply do this by executing with admin permissions the script named create_key_file
"""



import time,datetime,analysis,importlib,brokers

def broker_selection():
    '''Returns name of the selected broker
    
    '''
    broker_list=['kraken','binance']
    broker =''
    while broker not in broker_list:
        broker =str(input("Choose your broker:%s : "%broker_list))
    return broker

def create_key_file():
    broker = str(input("Enter your broker name :"))
    API_KEY = str(input("Enter your API key :"))
    SECRET_KEY = str(input("Enter your SECRET_KEY :"))
    file = open("C:\\"+broker+".key","w")
    file.write(API_KEY)
    file.write(SECRET_KEY)
    file.close()
    return
'''
broker_name = broker_selection()
broker = getattr(importlib.import_module('brokers'), '%s'%broker_name)
broker = broker()

try:
    file = open(r"C:\\" + str(broker_name) + ".key")
    file.close()
except:
    print("We are going to create the .key file")
    create_key_file()


path=r"C:\\" + str(broker_name) + ".key"
broker.connect_key(path)

rendement=1.010
'''
'''
Chossing kraken for developpement
'''
kraken=brokers.kraken()
kraken.connect_key('C:\\kraken.key')
binance=brokers.binance()
binance.connect_key('C:\\binance.key')
broker=brokers.kraken()
broker.connect_key('C:\\kraken.key')

class Timeout():
    '''Stores all the sensible data we need incase of connexion timout'''
    def __init__(self):
        self.buy=0.0
        self.sell=0.0
        self.crypto=0.0
        self.stable=0.0
Timeout=Timeout()

class Position():
    '''Stores all the data of the current openned position'''
    def __init__(self):
        self.price=0.0
        self.status='close'
        self.volume=0.0
        self.id=''
        self.level=1
Position=Position()



def open_position(symbol):
    '''Ouverture de la position'''
    '''On ouvre la position avec un stop loss prédéfinie''' 
    #broker.create_market_order(symbol='BTCEUR',side='buy',quantity=broker.balance(symbol)/broker.price['buy'])
    Position.status='open'    
    Position.level=1
    return 

def get_position_status():
    '''Verifie la situation de la position 
    '''
    if broker.get_open_orders()=={}:
        return ('close')
    else:
        return ('open')

def main():
    '''Main program function'''
    symbol='BTCEUR'
    #On initialise le temps de fonctionnement du programme
    start_time = time.time()
    print('Starting Trading:')
    up_time=0
    while(True):
        try:
            #Verifie la situation de la position
            Position.status = get_position_status()
            if Position.status=='close':
                #On actualise la librairie d'analyse afin de pouvoir changer la methode sans redémarrer le programme.
                try:
                    importlib.reload(analysis)
                    signal = analysis.buy_signal(symbol)
                except:
                    signal ='sell'
                    print('unable to get signal')
                #Si l'analyse donne un signal alors on place la position
                if signal=='buy':
                    open_position(symbol)
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