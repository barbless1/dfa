from random import *
from tkinter import *
from tkinter import ttk
from playsound import *


'''PARTIE 1 : interface graphique'''
class InterfaceGraphique:
    def __init__(self, master):
        self.master = master
        self.master.title("Fish dice adventure")
        self.master.geometry("720x1080")

        # Créer les éléments de l'interface
        self.label = Label(self.master, text="Bienvenue au jeu de dés !")
        self.label.pack(pady=10)

        self.button_lancer = Button(self.master, text="Lancer les dés", command=self.lancer_des)
        self.button_lancer.pack(pady=5)

        self.button_relancer = Button(self.master, text="Relancer les dés", command=self.relancer_des)
        self.button_relancer.pack(pady=5)

        self.resultat_label = Label(self.master, text="")
        self.resultat_label.pack(pady=10)

    def lancer_des(self):
        # Logique pour lancer les dés et afficher le résultat
        pass

    def relancer_des(self):
        # Logique pour relancer les dés sélectionnés et afficher le résultat
        pass



'''PARTIE 2 : logique du jeu'''
#valeur initial dès
class valeur_dès_initiale:
    def __init__(self):
        self.d1 = randint(1, 6)
        self.d2 = randint(1, 6)
        self.d3 = randint(1, 6)
        self.d4 = randint(1, 6)
        self.d5 = randint(1, 6)

#créer une liste des valeurs des dès
    def liste_valeurs_dès(self):
        return [self.d1, self.d2, self.d3, self.d4, self.d5]

#fonction pour relancer les dès
    def relancer_dès(self, dés_à_relancer):

'''PARTIE 3 : événements (appel des fonctions du jeu)'''
