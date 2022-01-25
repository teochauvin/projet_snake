from tkinter import *
from loop import *
from data import *

bg_color = "dark green"
size_app = "700x400"

class Menu :

    def __init__(self) :
        """
        Première fenetre de jeu
        """

        self.fenetre = Tk()
        self.fenetre.geometry(size_app)
        x, y = self.center(self.fenetre)

        self.fenetre.geometry(size_app + "+" + x + "+" + y)
        self.fenetre.title("Snake")
        self.fenetre.configure(bg = bg_color)

        self.loop = Loop()

        Label(self.fenetre, text='Menu principal', font=("Helvetica", 40), foreground = "White", bg = bg_color).pack(pady = 50)
        Button(self.fenetre, text = 'Jouer', width=60, height = 2, command = lambda : self.loop.JouerHumain(), bg = bg_color).pack(pady = 3)
        Button(self.fenetre, text = 'Intelligence artificielle', width=60, height = 2, command = self.fenetre_demonstration, bg = bg_color).pack(pady = 3)
        Button(self.fenetre, text = 'Quitter', width=60, height = 2, command = self.fenetre.destroy, bg = bg_color).pack(pady = 3)

        self.fenetre.mainloop()

    def fenetre_demonstration(self):
        """
        Fenetre de demonstration si on a appuyé sur intelligence atificielle
        """

        fenetre_secondaire = Toplevel(self.fenetre)
        fenetre_secondaire.geometry(size_app)
        x, y = self.center(fenetre_secondaire)

        fenetre_secondaire.geometry(size_app + "+" + x + "+" + y)
        fenetre_secondaire.configure(bg = bg_color)

        self.fenetre.withdraw()

        dossier = Dossier()

        Liste_qtable = []
        Liste_config = []

        nb_tables =  dossier.nombre_qtable
        nb_conf =  dossier.nombre_config

        for i in range(0, nb_tables + 1):

            if i == nb_tables:
                nom_qtable = "Nouvelle Qtable"
                Liste_qtable.append(nom_qtable)
            
            else:
                nom_qtable = "Qtable_{}".format(int(i))
                Liste_qtable.append(nom_qtable)

        for i in range(0, nb_conf + 1):

            if i == nb_conf:
                nom_config = "Nouvelle config"
                Liste_config.append(nom_config)                

            else:
                nom_config = "Config_{}".format(int(i))
                Liste_config.append(nom_config)
       
        Label(fenetre_secondaire, text='Sélectionner Qtable', font=("Helvetica", 20), foreground = "white", bg = bg_color).grid(row = 0, column = 0, pady = 10, padx = 20)

        deroulant_qtable = StringVar()
        deroulant_qtable.set(Liste_qtable[0])
        om_qtable = OptionMenu(fenetre_secondaire, deroulant_qtable, *Liste_qtable)
        om_qtable.grid(row = 0, column = 1)

        Label(fenetre_secondaire, text='Sélectionner Config', font=("Helvetica", 20), foreground = "white", bg = bg_color).grid(row = 1, pady = 10, padx = 20)

        deroulant_config = StringVar()
        deroulant_config.set(Liste_config[0])
        om_config = OptionMenu(fenetre_secondaire, deroulant_config, *Liste_config)
        om_config.grid(row = 1, column = 1)
        
        bouton_entrainer = Button(fenetre_secondaire, text = 'Entrainer', width=60, height = 2, command = lambda : entrainer(), bg = bg_color)
        bouton_entrainer.grid(row = 2, column = 0, pady = 10)
        bouton_demonstration = Button(fenetre_secondaire, text = 'Démonstration', width=60, height = 2, command = lambda : demonstration(), bg = bg_color)
        bouton_demonstration.grid(row = 3, column = 0, pady = 10)

        def entrainer():
            """
            Gestion des menus déroulants dans le cas ou on veut entrainer 
            """

            id_table = deroulant_qtable.get()

            if id_table == "Nouvelle Qtable":
                id_table = nb_tables
            
            else :
                id_table = int(id_table[7:])

            id_config = deroulant_config.get()

            if id_config == "Nouvelle config":
                id_config = nb_conf
            
            else :
                id_config = int(id_config[7:])

            self.loop.ProgrammeEntrainement(15, 100, detailler=True, id_qtable = id_table, id_config = id_config)

        def demonstration():
            """
                Gestion des menus déroulants dans le cas ou on veut faire la démo d'un qtable sur une config
            """

            id_table = deroulant_qtable.get()
            id_table = int(id_table[7:])
            id_config = deroulant_config.get()

            if id_config == "Nouvelle config":
                id_config = nb_conf
            
            else :
                id_config = int(id_config[7:])

            self.loop.DemonstrationAgent(id_config, id_table)

    def center(self, toplevel):
        """
            Centre la fenetre de jeu
        """

        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        size = size_app.split("x")

        x = screen_width//2 - int(size[0])//2
        y = screen_height//2 - int(size[1])//2

        return str(x), str(y)

if __name__ == "__main__" :
    menu = Menu()