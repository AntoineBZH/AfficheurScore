# -*-coding:Utf-8 -*-
import threading # Importe le module dédié à l'exécution parallèle
import serial # Importe le module dédié aux liaisons série
import io
import time # Importe le module dédié à la gestion du temps

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

        # Création et initialisation du flux de sortie
        self.outStream = bytes.fromhex(self._SerialPort.frameid) + " 0 318  0  010000000111222333    111222333         \r".encode('utf-8')

    def run(self):
        """Exécution du thread"""
        while not self.StopIsAsked: # permet de quitter le thread en cours
            self._SerialPort.write(self.outStream)
            time.sleep(0.1)
        
    def __del__(self):
        """Ferme le port série à la fin du thread"""
        self._SerialPort.close()
        if self._SerialPort.is_open:
            raise SerialException("Impossible de fermer le port {}.".format(self._SerialPort.port))

if __name__ == "__main__":
    TestSer = SimulSerial(port='COM2', frameid='30303035')
    TestSer.start()
