from random import *
from tkinter import *
from playsound import *

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
