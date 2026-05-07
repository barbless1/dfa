from random import * #Génération de pseudo-hasard pour les mécaniésmes reposant sur l'aléatoire (dés, case opening)
from tkinter import * #Moteur graphique / Interface from PIL import Image, ImageTk#from pyglet import * #Module utilisé pour le son 

'''PARTIE 0 : Application principale avec pages'''
class ApplicationPrincipale:
    def __init__(self, racine):
        self.racine = racine
        self.racine.geometry("1920x1080")
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
        bouton_jouer = Button(self, text="lancer !", font=("Helvetica", 14),
                             command=lambda: controleur.afficher_page(InterfaceGraphique),
                             width=20, height=2)
        bouton_jouer.pack(pady=20)
        bouton_jouer.place(x=1471, y=665)

        # bouton mon invetaire (aquarium)
        bouton_aquarium = Button(self, text="Mon aquarium", font=("Helvetica", 14), width=20, height=2, command=lambda: controleur.afficher_page(Aquarium))
        bouton_aquarium.pack(pady=20)
        bouton_aquarium.place(x=50, y=780)

        #bouton shop
        bouton_shop = Button(self, text="Shop", font=("Helvetica", 14), width=20, height=2, command=lambda: controleur.afficher_page(Shop))
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

        self.bouton_lancer = Button(self, text="Lancer les dés", font=("Helvetica", 18))
        self.bouton_lancer.pack(pady=5)
        
        #pour appeler la methode d'une autre classe, on doit d'abord créer une instance de cette classe, ici "jeu" est une instance de la classe "fonctions_du_jeu"
        self.jeu = fonctions_du_jeu(self) 
        self.bouton_lancer.config(command=self.jeu.lancer_des)
        self.bouton_lancer.place(x=1920/2-100, y=900)
        score = 0 
        self.etiquette_resultat = Label(self, text=f"score : {score}", font=("Helvetica", 40), fg="orange")
        self.etiquette_resultat.pack(pady=10) #pady signifie "padding y" pour ajouter de l'espace vertical entre les éléments ;)
        self.etiquette_resultat.place(x=10, y=10)

        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Helvetica", 14),
                                     command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=10, y=100)


        #mouvement main
        self.img_bras = PhotoImage(file='illustration/main_fermé.png')
        self.img_bras_ouverte = PhotoImage(file='illustration/main_ouverte.png')
        self.bras_id = self.canvas.create_image(200, 200, image=self.img_bras)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release_drag)

    def start_drag(self, event):
        self.last_x, self.last_y = event.x, event.y

    def drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.bras_id, dx, dy)
        self.last_x, self.last_y = event.x, event.y

    def release_drag(self, event):
        # Lancer les dés (qui gère aussi le changement d'image)
        self.jeu.lancer_des()

      
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
        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Helvetica", 14),
                                     command=lambda: controleur.afficher_page(PageAccueil))
        self.bouton_accueil.pack(pady=10)
        self.bouton_accueil.place(x=170, y=880)

class Aquarium(Frame):
    def __init__(self, parent, controleur):
        Frame.__init__(self, parent)
        self.controleur = controleur
        arriere_plan = PhotoImage(file='illustration/aquarium.png', master=racine)
        label_arriere_plan = Label(self, image=arriere_plan)
        label_arriere_plan.image = arriere_plan
        label_arriere_plan.place(relx=0.5, rely=0.5, anchor='center')

        # Bouton pour retourner à l'accueil
        self.bouton_accueil = Button(self, text="Retourner à l'accueil",font=("Helvetica", 14),
                                     command=lambda: controleur.afficher_page(PageAccueil))
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
        
        # Mettre à jour l'interface si elle est disponible
        if self.interface:
            self.interface.canvas.itemconfig(self.interface.bras_id, image=self.interface.img_bras_ouverte)
            self.interface.etiquette_resultat.config(text=f"score : {sum(self.liste_valeurs_dès())}")

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



'''PARTIE 4 : Lancement de l'application et événement '''
if __name__ == "__main__":
    racine = Tk()
    application = ApplicationPrincipale(racine)
    racine.mainloop()