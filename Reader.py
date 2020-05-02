# -*-coding:Utf-8 -*-
import threading # Importe le module dédié à l'exécution parallèle
import serial # Importe le module dédié aux liaisons série
import io
from time import sleep # Importe la méthode sleep pour la partie essai

class Reader(threading.Thread):
    """Thread chargé de récupérer et mettre en forme le flux de donnée sur la liaison série"""
        
    def __init__(self, port='COM2', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0, frameid='e0e4f835'):
        """Permet d'initialiser le thread et ouvrir le port série"""
        
        threading.Thread.__init__(self)
        
        # Initialisation des paramètres de la liaison série
        self._SerialPort = serial.Serial()
        self._SerialPort.port = port
        self._SerialPort.baudrate = baudrate
        self._SerialPort.bytesize = bytesize
        self._SerialPort.parity = parity
        self._SerialPort.stopbits = stopbits
        self._SerialPort.timeout = timeout
        self._SerialPort.xonxoff = xonxoff
        self._SerialPort.rtscts = rtscts
        self._SerialPort.frameid = frameid
        
        # Création d'un flag d'exécution
        self.StopIsAsked = False
        
        # Ouverture du port série
        self._SerialPort.open()
        if not self._SerialPort.is_open:
            raise SerialException("Impossible d\'instancier la classe Reader.")
            
        # Création d'un flux bufferisé de texte avec comme caractère de fin de ligne 0x0D
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._SerialPort, self._SerialPort), encoding='cp1252', newline='\r')

        # Création du flux de sortie
        self.outStream = "15:00|0|0|1|0|:|:|:|:|:|:"
        # Création d'un verrou sur le flux de sortie pour éviter les accès concurrents
        self.outLocker = threading.RLock()

    def run(self):
        """Exécution du thread"""
        while not self.StopIsAsked: # permet de quitter le thread en cours
            self._sio.flush()
            sMsgToDecode = "{}".format(self._sio.readline()) # récupère la trame
            if ((len(sMsgToDecode) == 56) and (sMsgToDecode[0:4].encode(self._sio.encoding).hex() == self._SerialPort.frameid)): # teste la trame selon sa longueur et sa trame d'identification
                sMsgToDecode = sMsgToDecode[4:] # supprime la trame d'identification qui ne contient pas d'information utile
                # Utilisation du gestionnaire de contexte avec un verrou pour éviter les accès concurrents
                with self.outLocker:
                    # Mise en forme de la trame dans le flux de sortie (temps, score locaux, score visiteurs, période, état chrono, locaux prison 1 à 3 et visiteurs prison 1 à 3)
                    self.outStream = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format("{}:{}".format(sMsgToDecode[2:4].lstrip(), sMsgToDecode[4:6]), sMsgToDecode[6:9].lstrip(), sMsgToDecode[9:12].lstrip(), sMsgToDecode[12], sMsgToDecode[18],\
                                    "{}:{}".format(sMsgToDecode[20], sMsgToDecode[21:23]).strip(), "{}:{}".format(sMsgToDecode[23], sMsgToDecode[24:26]).strip(), "{}:{}".format(sMsgToDecode[26], sMsgToDecode[27:29]).strip(), \
                                        "{}:{}".format(sMsgToDecode[33], sMsgToDecode[34:36]).strip(), "{}:{}".format(sMsgToDecode[36], sMsgToDecode[37:39]).strip(), "{}:{}".format(sMsgToDecode[39], sMsgToDecode[40:42]).strip())
        
    def __del__(self):
        """Ferme le port série à la fin du thread"""
        self._SerialPort.close()
        if self._SerialPort.is_open:
            raise SerialException("Impossible de fermer le port {}.".format(self._SerialPort.port))

if __name__ == "__main__":
    TestSer = Reader(port='/dev/ttyAMA0')
    TestSer.start()
    while True:
        print(TestSer.outStream)
        sleep(1)
