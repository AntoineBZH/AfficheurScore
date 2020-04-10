# -*-coding:Utf-8 -*-
import tkinter as tk    # importe le module dédié à l'interface graphique
import Reader           # importe le module gérant la communication avec l'afficheur
import io
import TcpServer        # importe le module gérant la communication avec le PC client

class GraphicInter(tk.Tk):
    """Thread chargé de récupérer le flux d'information du driver série et de l'afficher"""
        
    def __init__(self, ScreenPath):
        """Permet d'initialiser la fenêtre d'affichage et les flux d'informations du PC client et de l'afficheur"""

        super(GraphicInter, self).__init__()

        # Initialisation de la communication avec le PC client
        self.TcpClientCom = TcpServer.TcpServer()
        self.TcpClientCom.start()

        # Initialisation de la toile
        self.Screen = tk.PhotoImage(file=ScreenPath)
        self.ScreenWidth, self.ScreenHeight = self.Screen.width(), self.Screen.height()
        self.Canvas = tk.Canvas(self, width=self.ScreenWidth, height=self.ScreenHeight, borderwidth=0, highlightthickness=0)
        self.Canvas.pack()
        self.Canvas.create_image((self.ScreenWidth//2, self.ScreenHeight//2), image=self.Screen)

        # Propriétés de la fenêtre
        self.title('Broadcast')
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (self.ScreenWidth, self.ScreenHeight))

        # Initialisation du widget barre de score (position verticale, horizontale, hauteur, largeur)
        self.ScoreBarCoords = {'vert':32, 'horz':self.ScreenWidth//2, 'height':34, 'width':369}

        # Initialisation des champs et des cellules prisons (masquées par défaut)
        self._fieldLocalScore = self.Canvas.create_text(self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//13, self.ScoreBarCoords['vert'], text="0", font=("Arial", 13, 'bold'))
        self._fieldVisitorScore = self.Canvas.create_text(self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//13, self.ScoreBarCoords['vert'], text="0", font=("Arial", 13, 'bold'))
        self._fieldTime = self.Canvas.create_text(self.ScoreBarCoords['horz'], self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//10, text="15:00", font=("Arial", 9, 'bold'))
        self._fieldPeriod = self.Canvas.create_text(self.ScoreBarCoords['horz'], self.ScoreBarCoords['vert'] - self.ScoreBarCoords['height']//3.5, text="T M", font=("Arial", 8))
        self._LocalTeam = self.Canvas.create_text(self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.4, self.ScoreBarCoords['vert'], text="Equipe 1", fill='white', font=("Arial", 11, 'bold'), anchor='w')
        self._VisitorTeam = self.Canvas.create_text(self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.4, self.ScoreBarCoords['vert'], text="Equipe 2", fill='white', font=("Arial", 11, 'bold'), anchor='e')
        # Les champs prisons seront gérés sous forme de deux listes (une pour le texte et l'autre pour le fond) pour les ordonner
        self._pictLocalPrison = list()
        self._fieldLocalPrison = list()
        self._pictLocalPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5),  \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),       \
                                                              (self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5) + 26, \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,  \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldLocalPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5 + 13, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,     \
                                                              fill='white', state='hidden', font=("Arial", 8)))
        self._pictLocalPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5) + 35, \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),       \
                                                              (self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5) + 61, \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,  \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldLocalPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5 + 48, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,     \
                                                              fill='white', state='hidden', font=("Arial", 8)))
        self._pictLocalPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5) + 70, \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),       \
                                                              (self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5) + 96, \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,  \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldLocalPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] - self.ScoreBarCoords['width']//2.5 + 83, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,     \
                                                              fill='white', state='hidden', font=("Arial", 8)))
        self._pictVisitorPrison = list()
        self._fieldVisitorPrison = list()
        self._pictVisitorPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5) - 26,   \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),           \
                                                              (self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5),          \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,      \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldVisitorPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5 - 13, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,   \
                                                                fill='white', state='hidden', font=("Arial", 8)))
        self._pictVisitorPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5) - 61,   \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),           \
                                                              (self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5) - 35,     \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,      \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldVisitorPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5 - 48, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,   \
                                                                fill='white', state='hidden', font=("Arial", 8)))
        self._pictVisitorPrison.append(self.Canvas.create_rectangle((self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5) - 96,   \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2),           \
                                                              (self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5) -70,      \
                                                              (self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2) + 12,      \
                                                              width=0,fill='#285083', state='hidden'))
        self._fieldVisitorPrison.append(self.Canvas.create_text(self.ScoreBarCoords['horz'] + self.ScoreBarCoords['width']//2.5 - 83, self.ScoreBarCoords['vert'] + self.ScoreBarCoords['height']//2 + 6,   \
                                                                fill='white', state='hidden', font=("Arial", 8)))

        # Création d'une variable pour la gestion du temps mort
        self.TM = 'Game'

        # Lancement du thread de récupération des informations de l'afficheur
        self.PanelInfo = Reader.Reader(port='COM1', frameid='30303035')
        self.PanelInfo.start()

    def refresh(self):
        """Rafraichissement de l'écran"""
        # Récupération des données de l'application client
        sTcpRead = self.TcpClientCom.outStream.read()
        if sTcpRead != '':
            listSplitedTcpInfo = sTcpRead.split('|')
            if len(listSplitedTcpInfo) == 3:
                self.Canvas.itemconfigure(self._LocalTeam, text=listSplitedTcpInfo[0])
                self.Canvas.itemconfigure(self._VisitorTeam, text=listSplitedTcpInfo[1])
                self.TM = listSplitedTcpInfo[2]
                if self.TM == "TM":
                    self.Canvas.itemconfigure(self._fieldPeriod, text='T M')
        
        # Récupération des données de l'afficheur
        sPanelRead = self.PanelInfo.outStream.read()
        if sPanelRead != '':
            listSplitedPanelInfo = sPanelRead.split('|')
            # Mise en forme de l'affichage de la mi-temps ou d'un temps mort
            if self.TM != "TM":
                if listSplitedPanelInfo[3] == '1':
                    listSplitedPanelInfo[3] += 'ère'
                else:
                    listSplitedPanelInfo[3] += 'ème'
            else:
                listSplitedPanelInfo[3] = 'T M'
            self.Canvas.itemconfigure(self._fieldTime, text=listSplitedPanelInfo[0])
            self.Canvas.itemconfigure(self._fieldLocalScore, text=listSplitedPanelInfo[1])
            # Pour éviter que les champs d'affichage de score se superposent avec les champs chronomètre et mi-temps, diminution de la police de caractère si un des scores dépasse la centaine
            if len(listSplitedPanelInfo[1]) > 2 or len(listSplitedPanelInfo[2]) > 2:
                self.Canvas.itemconfigure(self._fieldLocalScore, font=("Arial", 10, 'bold'))
                self.Canvas.itemconfigure(self._fieldVisitorScore, font=("Arial", 10, 'bold'))
            else:
                self.Canvas.itemconfigure(self._fieldLocalScore, font=("Arial", 13, 'bold'))
                self.Canvas.itemconfigure(self._fieldVisitorScore, font=("Arial", 13, 'bold'))
            self.Canvas.itemconfigure(self._fieldVisitorScore, text=listSplitedPanelInfo[2])
            self.Canvas.itemconfigure(self._fieldPeriod, text=listSplitedPanelInfo[3])
            for index, item in enumerate(self._fieldLocalPrison):
                if listSplitedPanelInfo[5 + index] == ':':
                    self.Canvas.itemconfigure(item, state='hidden')
                    self.Canvas.itemconfigure(self._pictLocalPrison[index], state='hidden')
                else:
                    self.Canvas.itemconfigure(item, text=listSplitedPanelInfo[5 + index], state='normal')
                    self.Canvas.itemconfigure(self._pictLocalPrison[index], state='normal')
            for index, item in enumerate(self._fieldVisitorPrison):
                if listSplitedPanelInfo[8 + index] == ':':
                    self.Canvas.itemconfigure(item, state='hidden')
                    self.Canvas.itemconfigure(self._pictVisitorPrison[index], state='hidden')
                else:
                    self.Canvas.itemconfigure(item, text=listSplitedPanelInfo[8 + index], state='normal')
                    self.Canvas.itemconfigure(self._pictVisitorPrison[index], state='normal')
        self.after( 20, self.refresh)
    
    def close(self):
        """Arrêt des threads"""
        self.TcpClientCom.StopIsAsked = True
        self.PanelInfo.StopIsAsked = True
        self.TcpClientCom.join()
        self.PanelInfo.join()
        
if __name__ == "__main__":
    Disp = GraphicInter('Resources/modele.png')
    Disp.refresh()
    Disp.mainloop()
    Disp.close()
