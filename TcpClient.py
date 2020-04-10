# -*-coding:Utf-8 -*-
import socket           # Importe le module dédié au réseau
import tkinter as tk    # importe le module dédié à l'interface graphique

sHost = 'localhost'     # nom d'hôte ou adresse IP du serveur
iPort = 9600            # Port utilisé par la liaison TCP (entre 1024 et 65535)
iTeamNameMaxSize = 13   # Nombre maximum de caractères du nom des équipes (au-delà, le nom est tronqué)

class TcpClient(tk.Tk, socket.socket):
    """Thread chargé de récupérer et mettre en forme le flux de donnée sur la liaison série"""

    def __init__(self, *args, **kwargs):
        """Initialisation de la communication et ouverture de l'IHM"""

        # Renvoie les classes dont hérite TcpClient
        super(TcpClient, self).__init__(*args, **kwargs)

        # Initialisation de la partie réseau
        #   Construction du socket
        self.TcpConnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #   Connexion au serveur (Raspberry)
        self.TcpConnect.connect((sHost, iPort))

        bIsConnectionInitialized = False
        while not bIsConnectionInitialized:
            try:
                bIsConnectionInitialized = True
            #   Envoie d'une trame avec des valeurs initiales
                self.TcpConnect.send("Equipe 1|Equipe 2|Game".encode())
                if self.TcpConnect.recv(1024).decode() != '\n':
                    raise BufferError("Erreur d'acquitement du serveur")
            except ConnectionResetError:
                bIsConnectionInitialized = False

        # Initialisation de l'IHM
        self.title('Screen Controler')
        self.resizable(width=False, height=False)
        #   Création d'un cadre
        self.Frame = tk.Frame(self, width=330, height=140)
        self.Frame.pack(fill=tk.BOTH)
        self.Frame.pack_propagate(0)
        #   Bouton temps mort
        self.bIsOffTime = False
        self.sOffTime = "Game"
        self.buttTM = tk.Button(self.Frame, text="Temps mort", command=self.send, relief='raised', borderwidth=4, background='#9CDC57')
        self.buttTM.pack()
        self.buttTM.place(x=230, y=50)
        #   Ligne de saisie équipe domicile
        self.sLocalTeamName = tk.StringVar()
        self.labelLocalTeamName = tk.Label(self.Frame, text="Equipe 1")
        self.linLocalTeamName = tk.Entry(self.Frame, textvariable=self.sLocalTeamName, width=20, exportselection=0, relief='ridge', borderwidth=5)
        self.labelLocalTeamName.pack()
        self.labelLocalTeamName.place(x=10, y=30)
        self.linLocalTeamName.pack()
        self.linLocalTeamName.place(x=70, y=30)
        #   Ligne de saisie équipe extérieure
        self.sVisitTeamName = tk.StringVar()
        self.labelVisitTeamName = tk.Label(self.Frame, text="Equipe 2")
        self.linVisitTeamName = tk.Entry(self.Frame, textvariable=self.sVisitTeamName, width=20, exportselection=0, relief='ridge', borderwidth=5)
        self.labelVisitTeamName.pack()
        self.labelVisitTeamName.place(x=10, y=80)
        self.linVisitTeamName.pack()
        self.linVisitTeamName.place(x=70, y=80)
    
    def close(self):
        """Permet de fermer la connexion"""
        # Envoie le message de déconnexion
        self.TcpConnect.send("Quit".encode())
        if self.TcpConnect.recv(1024).decode() != '\n':
            raise BufferError("Erreur d'acquitement du serveur")

        # Fermeture de la connexion TCP
        self.TcpConnect.close()

    def send(self):
        """Evènement à chaque appuie sur le bouton Temps Mort"""
        self.bIsOffTime = not self.bIsOffTime
        if self.bIsOffTime:
            self.sOffTime = "TM"
            self.buttTM['relief']='sunken'
        else:
            self.sOffTime = "Game"
            self.buttTM['relief']='raised'
        # Envoie d'une trame de mise à jour
        self.TcpConnect.send("{}|{}|{}".format(self.sLocalTeamName.get()[:iTeamNameMaxSize], self.sVisitTeamName.get()[:iTeamNameMaxSize], self.sOffTime).encode())
        if self.TcpConnect.recv(1024).decode() != '\n':
            raise BufferError("Erreur d'acquitement du serveur")

    def refresh(self):
        """Rafraichissement de l'écran"""
        # Envoie d'une trame de mise à jour
        self.TcpConnect.send("{}|{}|{}".format(self.sLocalTeamName.get()[:iTeamNameMaxSize], self.sVisitTeamName.get()[:iTeamNameMaxSize], self.sOffTime).encode())
        if self.TcpConnect.recv(1024).decode() != '\n':
            raise BufferError("Erreur d'acquitement du serveur")
        self.after( 20, self.refresh)

if __name__ == "__main__":
    TcpClient = TcpClient()
    TcpClient.refresh()
    TcpClient.mainloop()
    TcpClient.close()
