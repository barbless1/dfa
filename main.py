from random import *
from tkinter import *
from playsound import *


'''PARTIE 0 : Application principale avec pages'''
class ApplicationPrincipale:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Fish dice adventure")
        self.racine.geometry("1080x720")
        
        # Créer un conteneur principal
        self.conteneur = Frame(self.racine)
        self.conteneur.pack(side="top", fill="both", expand=True)
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)
        
        self.cadres = {}
        
        # Ajouter les pages
        for F in (PageAccueil, InterfaceGraphique):
            cadre = F(self.conteneur, self)
            self.cadres[F] = cadre
            cadre.grid(row=0, column=0, sticky="nsew")
        
        # Afficher d'abord la page d'accueil
        self.afficher_page(PageAccueil)
    
    def afficher_page(self, contenu):
        cadre = self.cadres[contenu]
        cadre.tkraise()


'''PARTIE 1 : Page d'accueil'''
class PageAccueil(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        
        # Titre
        etiquette_titre = Label(self, text="Fish Dice Adventure", font=("Helvetica", 36, "bold"))
        etiquette_titre.pack(pady=50)
        
        # Sous-titre
        etiquette_sous_titre = Label(self, text="Bienvenue au jeu de lancer de dés !", font=("Helvetica", 16))
        etiquette_sous_titre.pack(pady=20)
        
        # Bouton pour démarrer le jeu
        bouton_jouer = Button(self, text="Jouer", font=("Helvetica", 14),
                             command=lambda: controleur.afficher_page(InterfaceGraphique),
                             width=20, height=2)
        bouton_jouer.pack(pady=20)
        
        # Bouton pour quitter
        bouton_quitter = Button(self, text="Quitter", font=("Helvetica", 14),
                               command=self.controleur.racine.quit,
                               width=20, height=2)
        bouton_quitter.pack(pady=10)


'''PARTIE 2 : interface graphique du jeu'''
class InterfaceGraphique(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur

        # Créer les éléments de l'interface
        self.etiquette = Label(self, text="Bienvenue au jeu de dés !", font=("Helvetica", 20, "bold"))
        self.etiquette.pack(pady=10)

        self.bouton_lancer = Button(self, text="Lancer les dés", command=self.lancer_des)
        self.bouton_lancer.pack(pady=5)

        self.bouton_relancer = Button(self, text="Relancer les dés", command=self.relancer_des)
        self.bouton_relancer.pack(pady=5)

        self.etiquette_resultat = Label(self, text="")
        self.etiquette_resultat.pack(pady=10)
        
        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retour à l'accueil", 
                                     command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)

    def lancer_des(self):
        # Logique pour lancer les dés et afficher le résultat
        pass

    def relancer_des(self):
        # Logique pour relancer les dés sélectionnés et afficher le résultat
        pass



'''PARTIE 3 : logique du jeu'''
#valeur initial dès
class valeur_dès_initiale:
    def __init__(self):
        self.de1 = randint(1, 6)
        self.de2 = randint(1, 6)
        self.de3 = randint(1, 6)
        self.de4 = randint(1, 6)
        self.de5 = randint(1, 6)

#créer une liste des valeurs des dès
    def liste_valeurs_dès(self):
        return [self.de1, self.de2, self.de3, self.de4, self.de5]

#fonction pour relancer les dès
    def relancer_dès(self, des_a_relancer):
        pass


'''PARTIE 4 : Lancement de l'application et événement '''
if __name__ == "__main__":
    racine = Tk()
    application = ApplicationPrincipale(racine)
    racine.mainloop()

