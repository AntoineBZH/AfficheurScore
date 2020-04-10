# -*-coding:Utf-8 -*-
import threading # Importe le module dédié à l'exécution parallèle
import serial # Importe le module dédié aux liaisons série
import io
import time # Importe le module dédié à la gestion du temps
import random # Importe le module dédié à l'aléatoire
import math # Importe le module dédié au mathématiques

class SimulSerial(threading.Thread):
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
        
        # Création des différents champs de la trame série
        TimeNow = math.trunc(time.time())
        self.LocalScore = 0
        self.VisitorScore = 0
        self.Time = "1500"
        self.Period = 1
        self.nbLocalPrison = random.randint(0, 3)
        self.nbVisitorPrison = random.randint(0, 3)
        
        # Création et initialisation du flux de sortie
        self.outStream = bytes.fromhex(self._SerialPort.frameid) + self.create_frame().encode('utf-8')
        
    def run(self):
        """Exécution du thread"""
        while not self.StopIsAsked: # permet de quitter le thread en cours
            if self.nbLocalPrison == 0 and self.nbVisitorPrison == 0:
                self.nbLocalPrison = random.randint(0, 3)
                self.nbVisitorPrison = random.randint(0, 3)
            self.outStream = bytes.fromhex(self._SerialPort.frameid) + self.create_frame().encode('utf-8')
            self._SerialPort.write(self.outStream)
            time.sleep(0.1)
    
    def create_frame(self):
        """Création de la trame à envoyer"""
    
        # Mise à jour des différents champs de la trame série
        TimeNow = math.trunc(time.time())
        
        # Ajout au hasard de 1 au score
        if (TimeNow % 120) == 100:
            self.LocalScore += random.choice([0, 0, 0, 0, 1])
            self.LocalScore %= 1000
        if (TimeNow % 120) == 40:
            self.VisitorScore += random.choice([0, 0, 0, 0, 1])
            self.VisitorScore %= 1000
        
        self.Time = str(time.localtime(900 - (TimeNow % 900)).tm_min).rjust(2) + "{:02d}".format(time.localtime(900 - (TimeNow % 900)).tm_sec) # 15:00 représente 900 sec
        if self.Time == ' 001':
            self.Period = (self.Period % 2) + 1
        
        LocalPrison = ""
        PrisonIter = 0
        while PrisonIter < self.nbLocalPrison:
            if (((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))) != 1:
                LocalPrison += (str(time.localtime(((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))).tm_min) + "{:02d}".format(time.localtime(((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))).tm_sec))
            PrisonIter +=1
        self.nbLocalPrison = len(LocalPrison) // 3

        VisitorPrison = ""
        PrisonIter = 0
        while PrisonIter < self.nbVisitorPrison:
            if  (((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))) != 1:
                VisitorPrison += (str(time.localtime(((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))).tm_min) + "{:02d}".format(time.localtime(((3 - PrisonIter) * 60) - (TimeNow % ((3 - PrisonIter) * 60))).tm_sec))
            PrisonIter +=1
        self.nbVisitorPrison = len(VisitorPrison) // 3
        
        return "{}{}{}{}{}{}{}{}{}{}{}{}".format(" 0", self.Time, str(self.LocalScore).rjust(3), str(self.VisitorScore).rjust(3),
                        str(self.Period), str(self.nbLocalPrison), str(self.nbVisitorPrison), "00000", LocalPrison.ljust(9), "    ", VisitorPrison.ljust(9), "         \r")
        
    def __del__(self):
        """Ferme le port série à la fin du thread"""
        self._SerialPort.close()
        if self._SerialPort.is_open:
            raise SerialException("Impossible de fermer le port {}.".format(self._SerialPort.port))

if __name__ == "__main__":
    TestSer = SimulSerial(port='COM1', frameid='30303035')
    TestSer.start()
    while True:
        print(TestSer.outStream)
        time.sleep(1)
