import os
from random import * #Génération de pseudo-hasard pour les mécaniésmes reposant sur l'aléatoire (dés, case opening)
from tkinter import * #Moteur graphique / Interface from PIL import Image, ImageTk#from pyglet import * #Module utilisé pour le son 
#from simpleaudio import * #https://www.piwheels.org/project/simpleaudio/ nécessite alsa et Clang sur linux, tranquille sur windows je crois 

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
        self.monnaie = 0
        self.achats = set()
        self.poissons = self.charger_poissons()
        
        # Ajouter les pages
        for F in (PageAccueil, InterfaceGraphique, Shop, Aquarium): #ajouter les autres pages ici AU FUR ET À MESURE
            cadre = F(self.conteneur, self)
            self.cadres[F] = cadre
            cadre.grid(row=0, column=0, sticky="nsew")
        
        # Afficher d'abord la page d'accueil
        self.afficher_page(PageAccueil)
    
    def afficher_page(self, contenu):
        cadre = self.cadres[contenu]
        if hasattr(cadre, "rafraichir"):
            cadre.rafraichir()
        cadre.tkraise()

    def charger_poissons(self):
        dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "illustration", "poisson")
        fichiers = [f for f in os.listdir(dossier) if f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))]
        fichiers.sort()
        items = []
        for index, fichier in enumerate(fichiers):
            nom = os.path.splitext(fichier)[0]
            prix = 200 + 50 * index
            items.append({"fichier": fichier, "nom": nom, "prix": prix})
        return items


'''PARTIE 1 : Page d'accueil'''
class PageAccueil(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/interface_partie_FDA.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan  # Garder une référence pour éviter que l'image ne soit supprimée
        label_arriere_plan.place(x=0, y=0, relwidth=1, relheight=1)
        #Simpleaudio fond début jeu 
    
        
        # Bouton pour démarrer le jeu
        bouton_jouer = Button(self, text="Lancer", font=("Arial", 14),
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

        self.etiquette_combinaison = Label(self, text="Combinaison : -", font=("Arial", 18), fg="blue")
        self.etiquette_combinaison.place(x=1920 / 2, y=1080 / 2 + 300)
        self.etiquette_score = Label(self, text="Score : -", font=("Arial", 18), fg="blue")
        self.etiquette_score.place(x=1920 / 2, y=1080 / 2 + 340)
        self.etiquette_monnaie = Label(self, text=f"Monnaie : {self.controleur.monnaie} points", font=("Arial", 18), fg="black")
        self.etiquette_monnaie.place(x=10, y=180)

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
        self.score_ajoute = False

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
            self.lancees_restantes = 2
            self.score_ajoute = False
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
            texte_id = self.canvas.create_text(x + 25, y + 25, text=str(valeur), font=("Arial", 18))
            self.des_ids.extend([des_id, texte_id])

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

    def update_monnaie_label(self):
        self.etiquette_monnaie.config(text=f"Monnaie : {self.controleur.monnaie} points")

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
            return
        for i in range(5):
            if not self.des_gardes[i]:
                self.valeurs_des[i] = randint(1, 6)
        self.lancees_restantes -= 1
        self.afficher_des()

        if self.lancees_restantes <= 0:
            self.afficher_resultat()

    def nom_combinaison(self):
        valeurs = sorted(self.valeurs_des)
        frequence = {val: valeurs.count(val) for val in set(valeurs)}
        counts = sorted(frequence.values())
        est_suite = len(set(valeurs)) == 5 and valeurs[-1] - valeurs[0] == 4

        if counts == [5]:
            return "Yams"
        if est_suite:
            return "Suite"
        if counts == [2, 3]:
            return "Full"
        if counts == [1, 4]:
            return "Carré"
        if counts == [1, 1, 3]:
            return "Brelan"
        if counts == [1, 2, 2]:
            return "Double paire"
        if counts == [1, 1, 1, 2]:
            return "Paire"
        return "Chance"

    def afficher_resultat(self):
        """Affiche la combinaison finale et le score."""
        combinaison = ", ".join(map(str, self.valeurs_des))
        score = sum(self.valeurs_des)
        self.etiquette_combinaison.config(text=f"Combinaison : {self.nom_combinaison()} ({combinaison})")
        self.etiquette_score.config(text=f"Score : {score}")
        self.etiquette_resultat.config(text=f"{score} points")
        if not self.score_ajoute:
            self.controleur.monnaie += score
            self.score_ajoute = True
            self.update_monnaie_label()

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
        self.etiquette_combinaison.config(text="Combinaison : -")
        self.etiquette_score.config(text="Score : -")
        self.etiquette_resultat.config(text="0 points")
        self.score_ajoute = False

      
'''BOUTIQUE DU JEU : page du shop'''
class Shop(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/shop.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan
        label_arriere_plan.place(relx=0.5, rely=0.5, anchor='center')

        self.etiquette_monnaie = Label(self, text=f"Monnaie : {self.controleur.monnaie} points", font=("Arial", 18), fg="black", bg="white")
        self.etiquette_monnaie.place(x=715, y=20)
        self.info_achat = Label(self, text="", font=("Arial", 14), fg="red", bg="white")
        self.info_achat.place(x=980, y=20)

        # Rendre la zone d'achat visuellement 'transparente' en reprenant le fond parent
        self.zone_achat = Frame(self, bg=parent.cget('bg'), bd=0, relief='flat', highlightthickness=0)
        self.zone_achat.place(x=715, y=45, width=1157, height=768)

        self.poisson_images = []
        self.poisson_buttons = []

        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Arial", 14), command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=165, y=880)

    def rafraichir(self):
        self.etiquette_monnaie.config(text=f"Monnaie : {self.controleur.monnaie} points")
        self.info_achat.config(text="")
        for child in self.zone_achat.winfo_children():
            child.destroy()
        self.poisson_images = []
        self.poisson_buttons = []

        for idx, item in enumerate(self.controleur.poissons):
            row = idx // 4
            col = idx % 4
            item_frame = Frame(self.zone_achat, width=250, height=280)
            item_frame.grid(row=row, column=col, padx=10, pady=10)
            item_frame.grid_propagate(False)
            item_frame.pack_propagate(False)

            chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "illustration", "poisson", item["fichier"])
            img = PhotoImage(file=chemin)
            self.poisson_images.append(img)
            label_img = Label(item_frame, image=img, bg="white")
            label_img.pack(padx=5, pady=(5, 0))
            label_nom = Label(item_frame, text=item["nom"], font=("Arial", 14), bg="white")
            label_nom.pack()
            label_prix = Label(item_frame, text=f"{item['prix']} pts", font=("Arial", 12), bg="white")
            label_prix.pack()

            if item["fichier"] in self.controleur.achats:
                btn = Button(item_frame, text="Acheté", state="disabled", width=14)
            else:
                btn = Button(item_frame, text=f"Acheter ({item['prix']} pts)", command=lambda idx=idx: self.acheter_poisson(idx), width=14)
            btn.pack(pady=5)
            self.poisson_buttons.append(btn)

        for i in range(4):
            self.zone_achat.grid_columnconfigure(i, weight=1)

    def acheter_poisson(self, index):
        item = self.controleur.poissons[index]
        if item["fichier"] in self.controleur.achats:
            return
        if self.controleur.monnaie < item["prix"]:
            self.info_achat.config(text="Pas assez de points pour cet achat.")
            return
        self.controleur.monnaie -= item["prix"]
        self.controleur.achats.add(item["fichier"])
        self.info_achat.config(text=f"Poisson {item['nom']} acheté !")
        self.rafraichir()


'''AQUARIUM : Inventaire des poissons obtenus'''
class Aquarium(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/aquarium.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan
        label_arriere_plan.place(relx=0.5, rely=0.5, anchor='center')

        self.zone_aquarium = Frame(self, bg=None, bd=0, relief='flat', highlightthickness=0)
        self.zone_aquarium.place(x=715, y=45, width=1157, height=768)
        self.aquarium_images = []

        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Arial", 14), command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=165, y=800)

    def rafraichir(self):
        for child in self.zone_aquarium.winfo_children():
            child.destroy()
        self.aquarium_images = []

        achats = list(self.controleur.achats)
        if not achats:
            Label(self.zone_aquarium, text="Aucun poisson acheté.", font=("Arial", 18), bg="white").place(relx=0.5, rely=0.5, anchor='center')
            return

        for idx, fichier in enumerate(achats):
            row = idx // 4
            col = idx % 4
            item_frame = Frame(self.zone_aquarium, width=250, height=280, bg="white")
            item_frame.grid(row=row, column=col, padx=10, pady=10)
            item_frame.grid_propagate(False)
            item_frame.pack_propagate(False)

            chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "illustration", "poisson", fichier)
            img = PhotoImage(file=chemin)
            self.aquarium_images.append(img)
            label_img = Label(item_frame, image=img, bg="white")
            label_img.pack(padx=5, pady=(5, 0))
            label_nom = Label(item_frame, text=os.path.splitext(fichier)[0], font=("Arial", 14), bg="white")
            label_nom.pack()

        for i in range(4):
            self.zone_aquarium.grid_columnconfigure(i, weight=1)

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
            combinaisons.append(("Yams", 200))
        if self.est_carré():
            combinaisons.append(("Carré", sum(self.liste_valeurs_dès())))
        if self.est_full():
            combinaisons.append(("Full", 50))
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