# -*-coding:Utf-8 -*-
import threading    # Importe le module dédié à l'exécution parallèle
import socket       # Importe le module dédié au réseau

class TcpServer(threading.Thread):
    """Thread chargé de gérer la liaison TCP avec le PC client"""
        
    def __init__(self, port=9600):
        """Permet d'initialiser le thread et créer le serveur TCP"""
        
        threading.Thread.__init__(self)
        
        # Construction du socket
        self._TcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        
        # Connexion du socket
        self._TcpServer.bind(('', self.port))
        self._TcpServer.listen(5)
        
        # Création d'un flag d'exécution
        self.StopIsAsked = False

        # Création du flux de sortie
        self.outStream = "Equipe 1|Equipe 2|Game"
        # Création d'un verrou sur le flux de sortie pour éviter les accès concurrents
        self.outLocker = threading.RLock()

    def run(self):
        """Exécution du thread"""
        
        # Attente de connexion du PC client
        self._ClientConnection, self._InfosConnection = self._TcpServer.accept()

        while not self.StopIsAsked: # permet de quitter le thread en cours
            try:
                sMsgReceived = "{}".format(self._ClientConnection.recv(1024).decode()) # récupère la trame
                # Si reception d'un message Quit, l'IHM client a été fermé
                if sMsgReceived == "Quit":
                    # Acquitement du message
                    self._ClientConnection.send(b"\n")
                    self._ClientConnection.close()
                    # Attente d'une nouvelle connexion du PC client
                    self._ClientConnection, self._InfosConnection = self._TcpServer.accept()
                # Message envoyé dans le flux de sortie pour l'interface graphique
                elif (len(sMsgReceived) != 0): # teste le message reçu n'est pas vide
                    # Acquitement du message
                    self._ClientConnection.send(b"\n")
                    # Mise à jour de la trame reçue par le PC client pour affichage dans le gestionnaire de contexte pour éviter les accès concurrents
                    with self.outLocker:
                        self.outStream = sMsgReceived
            except ConnectionResetError:
                self._ClientConnection.close()
                # Attente d'une nouvelle connexion du PC client
                self._ClientConnection, self._InfosConnection = self._TcpServer.accept()
        
    def __del__(self):
        """Ferme la connexion"""
        self._ClientConnection.close()
        self._TcpServer.close()
