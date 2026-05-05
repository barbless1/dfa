from random import *
from tkinter import *
# from ... import * (librairie de son manquante, à décider plus tard )

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
        arriere_plan = PhotoImage(file='illustration/arrière plan.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan  # Garder une référence pour éviter que l'image ne soit supprimée
        label_arriere_plan.place(x=0, y=0, relwidth=1, relheight=1)
    
        
        # Bouton pour démarrer le jeu
        bouton_jouer = Button(self, text="Jouer", font=("Helvetica", 14),
                             command=lambda: controleur.afficher_page(InterfaceGraphique),
                             width=20, height=2)
        bouton_jouer.pack(pady=20)
        bouton_jouer.place(x=1471, y=665)

        # bouton mon invetaire (aquarium)
        bouton_aquarium = Button(self, text="Mon aquarium", font=("Helvetica", 14), width=20, height=2)
                                # command= A ECRIRE 
        bouton_aquarium.pack(pady=20)
        bouton_aquarium.place(x=462, y=545)

'''PARTIE 2 : interface graphique du jeu'''
class InterfaceGraphique(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur

        self.bouton_lancer = Button(self, text="Lancer les dés", command=self.lancer_des)
        self.bouton_lancer.pack(pady=5)


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
   # def relancer_dès(self, des_a_relancer):
    


'''PARTIE 4 : Lancement de l'application et événement '''
if __name__ == "__main__":
    racine = Tk()
    application = ApplicationPrincipale(racine)
    racine.mainloop()