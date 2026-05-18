from random import * #Génération de pseudo-hasard pour les mécaniésmes reposant sur l'aléatoire (dés, case opening)
from tkinter import * #Moteur graphique / Interface from PIL import Image, ImageTk#from pyglet import * #Module utilisé pour le son 

'''PARTIE 0 : Application principale avec pages'''
class ApplicationPrincipale:
    def __init__(self, racine):
        self.racine = racine
        self.racine.geometry("1895x960") #Taille de la fenêtre accordée avec la taille de interface_partie_FDA.png 
        icon = PhotoImage(file="illustration/icone.png") #.ico est une extension propre à windows, pour que ça marche sur tous les systèmes, on utilise .png 
        self.racine.iconphoto(True, icon)

        # Créer un conteneur principal
        self.conteneur = Frame(self.racine)
        self.conteneur.pack(side="top", fill="both", expand=True)
        self.conteneur.grid_rowconfigure(0, weight=1)
        self.conteneur.grid_columnconfigure(0, weight=1)
        
        self.cadres = {}
        
        # Ajouter les pages
        for F in (PageAccueil, InterfaceGraphique, Shop, Aquarium): #ajouter les autres pages ici AU FUR ET À MESURE
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
        arriere_plan = PhotoImage(file='illustration/interface_partie_FDA.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan  # Garder une référence pour éviter que l'image ne soit supprimée
        label_arriere_plan.place(x=0, y=0, relwidth=1, relheight=1)
    
        
        # Bouton pour démarrer le jeu
        bouton_jouer = Button(self, text="lancer !", font=("Arial", 14),
                             command=lambda: controleur.afficher_page(InterfaceGraphique),
                             width=20, height=2)
        bouton_jouer.pack(pady=20)
        bouton_jouer.place(x=1471, y=665)

        # bouton mon invetaire (aquarium)
        bouton_aquarium = Button(self, text="Mon aquarium", font=("Arial", 14), width=20, height=2, command=lambda: controleur.afficher_page(Aquarium))
        bouton_aquarium.pack(pady=20)
        bouton_aquarium.place(x=50, y=780)

        #bouton shop
        bouton_shop = Button(self, text="Shop", font=("Arial", 14), width=20, height=2, command=lambda: controleur.afficher_page(Shop))
        bouton_shop.pack(pady=20)
        bouton_shop.place(x=50, y=850)

      
'''PARTIE 2 : interface graphique du jeu'''
class InterfaceGraphique(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        self.canvas = Canvas(self)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        arriere_plan = PhotoImage(file='illustration/tronc_arbre_zoom.png')
        self.canvas.create_image(0, 0, image=arriere_plan, anchor='nw')
        self.arriere_plan = arriere_plan

        score = 0
        self.etiquette_resultat = Label(self, text=f"{score} points", font=("Arial", 40), fg="black")
        self.etiquette_resultat.pack(pady=10)
        self.etiquette_resultat.place(x=10, y=10)

        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retourner à l'accueil", font=("Arial", 14),
                                     command=lambda: [self.reset_page(), controleur.afficher_page(PageAccueil)])
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=10, y=100)

        # Bouton pour relancer les dés
        self.bouton_relancer = Button(self, text="Relancer les dés", font=("Arial", 14),
                                      command=self.preparer_relance, state="disabled")
        self.bouton_relancer.pack(pady=10)
        self.bouton_relancer.place(x=1920 / 2 - 100, y=1080 / 2 + 150)

        # Mouvement main
        self.img_bras = PhotoImage(file='illustration/main_fermé.png')
        self.img_bras_ouverte = PhotoImage(file='illustration/main_ouverte.png')
        self.bras_id = self.canvas.create_image(1920 / 2, 1080 / 2, image=self.img_bras)
        self.canvas.coords(self.bras_id, 1920 / 2, 1080 / 2)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release_drag)

        # État du jeu
        self.valeurs_des = []
        self.des_gardes = [False] * 5
        self.lancer_effectue = False
        self.lancees_restantes = 3
        self.relaunch_ready = False
        self.drag_active = False
        self.des_ids = []
        self.boutons_garder = []

    def start_drag(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.drag_active = True

    def drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.bras_id, dx, dy)
        self.last_x, self.last_y = event.x, event.y

    def release_drag(self, event):
        if not self.drag_active:
            return
        self.drag_active = False
        self.canvas.itemconfig(self.bras_id, image=self.img_bras_ouverte)

        if not self.lancer_effectue:
            self.valeurs_des = [randint(1, 6) for _ in range(5)]
            self.des_gardes = [False] * 5
            self.lancees_restantes = 3
            self.afficher_des()
            self.lancer_effectue = True
            self.bouton_relancer.config(state="normal")
        elif self.relaunch_ready:
            self.relaunch_ready = False
            self.relancer_non_gardes()

    def afficher_des(self):
        """Affiche les dés avec leurs valeurs actuelles."""
        self.clear_des()
        x, y = 1920 / 2 - 150, 1080 / 2 - 50
        for i, valeur in enumerate(self.valeurs_des):
            couleur = "green" if self.des_gardes[i] else "white"
            des_id = self.canvas.create_rectangle(x, y, x + 50, y + 50, fill=couleur)
            self.canvas.create_text(x + 25, y + 25, text=str(valeur), font=("Arial", 18))
            self.des_ids.append(des_id)

            bouton = Button(self, text="Garder", command=lambda idx=i: self.garder_de(idx))
            bouton.place(x=x + 10, y=y + 60)
            self.boutons_garder.append(bouton)

            x += 60

    def clear_des(self):
        for des_id in self.des_ids:
            self.canvas.delete(des_id)
        self.des_ids = []
        for bouton in self.boutons_garder:
            bouton.destroy()
        self.boutons_garder = []

    def garder_de(self, index):
        """Marque un dé comme gardé ou non."""
        self.des_gardes[index] = not self.des_gardes[index]
        self.afficher_des()

    def preparer_relance(self):
        if not self.lancer_effectue or self.lancees_restantes <= 0:
            return
        self.relaunch_ready = True
        self.canvas.itemconfig(self.bras_id, image=self.img_bras)

    def relancer_non_gardes(self):
        if self.lancees_restantes <= 0:
            self.afficher_resultat()
            return
        for i in range(5):
            if not self.des_gardes[i]:
                self.valeurs_des[i] = randint(1, 6)
        self.lancees_restantes -= 1
        self.afficher_des()

        if self.lancees_restantes <= 0:
            self.afficher_resultat()

    def afficher_resultat(self):
        """Affiche la combinaison finale et le score."""
        combinaison = "-".join(map(str, self.valeurs_des))
        score = sum(self.valeurs_des)
        self.canvas.create_text(1920 / 2, 1080 / 2 + 300, text=f"Combinaison : {combinaison}\nScore : {score}",
                                 font=("Arial", 18), fill="blue")

    def reset_page(self):
        """Réinitialise la page de lancer de dés."""
        self.canvas.coords(self.bras_id, 1920 / 2, 1080 / 2)
        self.canvas.itemconfig(self.bras_id, image=self.img_bras)
        self.clear_des()
        self.lancer_effectue = False
        self.lancees_restantes = 3
        self.relaunch_ready = False
        self.des_gardes = [False] * 5
        self.valeurs_des = []
        self.bouton_relancer.config(state="disabled")

      
'''BOUTIQUE DU JEU : page du shop'''
class Shop(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/shop.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan  # Garder une référence pour éviter que l'image ne soit supprimée
        label_arriere_plan.place(relx=0.5, rely=0.5, anchor='center') 

        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Arial", 14), command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=165, y=880)


        
'''AQUARIUM : Inventaire des poissons obtenus'''
class Aquarium(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/aquarium.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan
        label_arriere_plan.place(relx=0.5, rely=0.5, anchor='center')

        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Arial", 14), command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=165, y=800)

'''PARTIE 3 : logique du jeu'''
#valeur initial dès
class fonctions_du_jeu:
    def __init__(self, interface=None):
        self.interface = interface
        self.de1 = randint(1, 6)
        self.de2 = randint(1, 6)
        self.de3 = randint(1, 6)
        self.de4 = randint(1, 6)
        self.de5 = randint(1, 6)

#créer une liste des valeurs des dès
    def liste_valeurs_dès(self):
        return [self.de1, self.de2, self.de3, self.de4, self.de5]

#fonction pour relancer les dès
    
    def lancer_des(self):
        # Logique pour lancer les dés et afficher le résultat
        self.de1 = randint(1, 6)
        self.de2 = randint(1, 6)
        self.de3 = randint(1, 6)
        self.de4 = randint(1, 6)
        self.de5 = randint(1, 6)
        
        
    def relancer_des(self, des_a_relancer):
        """
        Relance les dés spécifiés par leurs indices.
        des_a_relancer: Liste des indices des dés à relancer (1 à 5).
        """
        for index in des_a_relancer:
            if index == 1:
                self.de1 = randint(1, 6)
            elif index == 2:
                self.de2 = randint(1, 6)
            elif index == 3:
                self.de3 = randint(1, 6)
            elif index == 4:
                self.de4 = randint(1, 6)
            elif index == 5:
                self.de5 = randint(1, 6)

    # FONCTIONS POUR DÉTERMINER LES COMBINAISONS DU YAMS
    
    def est_yams(self):
        """Vérifie si c'est un Yams (5 dés identiques)"""
        dés = self.liste_valeurs_dès()
        return len(set(dés)) == 1
    
    def est_carré(self):
        """Vérifie si c'est un Carré (4 dés identiques)"""
        dés = self.liste_valeurs_dès()
        compte = {}
        for d in dés:
            compte[d] = compte.get(d, 0) + 1
        return 4 in compte.values()
    
    def est_full(self):
        """Vérifie si c'est un Full (3 d'une valeur + 2 d'une autre)"""
        dés = self.liste_valeurs_dès()
        compte = {}
        for d in dés:
            compte[d] = compte.get(d, 0) + 1
        valeurs = sorted(compte.values())
        return valeurs == [2, 3]
    
    def est_grande_suite(self):
        """Vérifie si c'est une Grande Suite (5 dés consécutifs)"""
        dés = sorted(self.liste_valeurs_dès())
        # Petite suite: [1,2,3,4,5] ou [2,3,4,5,6]
        return dés == [1, 2, 3, 4, 5] or dés == [2, 3, 4, 5, 6]
    
    def est_petite_suite(self):
        """Vérifie si c'est une Petite Suite (4 dés consécutifs)"""
        dés = set(self.liste_valeurs_dès())
        petites_suites = [
            {1, 2, 3, 4},
            {2, 3, 4, 5},
            {3, 4, 5, 6}
        ]
        for suite in petites_suites:
            if suite.issubset(dés): #cette focntion est incroyable elle vérifie si la condition s'applique et renvoie True 
                return True
        return False
    
    def est_brelan(self):
        """Vérifie si c'est un Brelan (3 dés identiques)"""
        dés = self.liste_valeurs_dès()
        compte = {}
        for d in dés:
            compte[d] = compte.get(d, 0) + 1
        return 3 in compte.values()
    
    def est_deux_paires(self):
        """Vérifie si c'est deux paires"""
        dés = self.liste_valeurs_dès()
        compte = {}
        for d in dés:
            compte[d] = compte.get(d, 0) + 1
        paires = [v for v in compte.values() if v == 2]
        return len(paires) == 2
    
    def est_paire(self):
        """Vérifie s'il y a une paire (2 dés identiques)"""
        dés = self.liste_valeurs_dès()
        compte = {}
        for d in dés:
            compte[d] = compte.get(d, 0) + 1
        return 2 in compte.values()
    
    def compter_valeur(self, valeur):
        """Compte le nombre de dés ayant une valeur spécifique"""
        dés = self.liste_valeurs_dès()
        return dés.count(valeur) * valeur
    
    def chance(self):
        """Retourne la somme de tous les dés"""
        return sum(self.liste_valeurs_dès())
    
    def determiner_combinaison(self):
        """Détermine la meilleure combinaison et retourne son nom et sa valeur"""
        combinaisons = []
        
        if self.est_yams():
            combinaisons.append(("Yams", 50))
        if self.est_carré():
            combinaisons.append(("Carré", sum(self.liste_valeurs_dès())))
        if self.est_full():
            combinaisons.append(("Full", 25))
        if self.est_grande_suite():
            combinaisons.append(("Grande Suite", 40))
        if self.est_petite_suite():
            combinaisons.append(("Petite Suite", 30))
        if self.est_brelan():
            combinaisons.append(("Brelan", sum(self.liste_valeurs_dès())))
        if self.est_deux_paires():
            combinaisons.append(("Deux Paires", sum(self.liste_valeurs_dès())))
        if self.est_paire():
            combinaisons.append(("Paire", sum(self.liste_valeurs_dès())))
        
        # Ajouter les combinaisons spéciales (1 à 6)
        for valeur in range(1, 7):
            total = self.compter_valeur(valeur)
            if total > 0:
                noms = {1: "As", 2: "Deux", 3: "Trois", 4: "Quatre", 5: "Cinq", 6: "Six"}
                combinaisons.append((noms[valeur], total))
        
        # Ajouter chance
        combinaisons.append(("Chance", self.chance()))
        
        return combinaisons
    
    def meilleure_combinaison(self):
        """Retourne la meilleure combinaison par valeur"""
        combinaisons = self.determiner_combinaison()
        if combinaisons:
            return max(combinaisons, key=lambda x: x[1])
        return ("Rien", 0)

    


'''PARTIE 4 : Lancement de l'application et événement '''
if __name__ == "__main__":
    racine = Tk()
    application = ApplicationPrincipale(racine)
    racine.mainloop()