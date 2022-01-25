from random import randint
import os
import numpy as np

class QTable: 

    def __init__(self, id=1):
        """
            La QTable à un certain nombre d'état
            Un chemin d'accès
            On l'initialise si elle n'existe pas, sinon on la charge
        """

        self.nEtat = 64
        self.path = "qtables/q_{}".format(id) 

        if not os.path.exists(self.path):
            print("Qtable créé et initilisée à 0")
            self.Q = [[0.0, 0.0, 0.0] for _ in range(self.nEtat)]
        else: 
            print("Qtable chargée")
            self.Q = self.ChargeQTable()

    def SauvegardeQTable(self, debug=True):
        """
            Permet d'aller écrire dans le fichier texte correspondant
        """
        with open(self.path, 'w') as f: 
            for i in range(self.nEtat):
                f.write("{},{},{}\n".format(self.Q[i][0],self.Q[i][1],self.Q[i][2]))

    def ChargeQTable(self): 
        """
            Va lire et décode le fichier texte correspondant
        """
        
        Q = []

        with open(self.path, 'r') as f: 
            lignes = f.readlines()

            for ligne in lignes:
                tab = [] 

                for c in ligne.split(","): 
                    tab.append(float(c))

                Q.append(tab)

        return Q
    
    def get_DetailsQTable(self):
        """
            Méthode qui verbalise la QTable de manière humainement compréhensible
            Fichier de 64 lignes
        """ 

        mouvement = ["gauche", "devant", "droite"]

        etat = [
            "Derriere", 
            "Derriere à Droite", 
            "Droite", 
            "Devant à Droite", 
            "Devant", 
            "Devant à Gauche", 
            "Gauche", 
            "Derriere à Gauche"
        ]

        danger = [
            "Nul part", 
            "Gauche", 
            "Devant", 
            "Gauche et Devant", 
            "Droite", 
            "Droite et Gauche", 
            "Droite et Devant", 
            "Partout"
        ]

        with open("qtables/debug", 'w') as f: 

            for i in range(self.nEtat): 
                etat_id = i//8
                danger_id = i%8
                mouvement_id = np.argmax(self.Q[i]) 

                f.writelines("La nourriture se situe {} le dangers est {}, snake decide de {}\n".format(etat[etat_id], danger[danger_id], mouvement[mouvement_id]))


class Configs: 

    def __init__(self, taille_memoire, id=1):
        """
            Une config est une liste de nombres extraite d'un fichier situe au chemin d'accès indiqué
            Si elle existe pas on la fabrique
        """

        self.config = []
        self.path = "configs/conf_{}.cf".format(int(id))
        self.longueur = taille_memoire**2

        if not os.path.exists(self.path):
            self.build_file()

    def get(self): 
        """
            Va lire et charge la config
        """

        lecture = [] 

        with open(self.path, 'r') as f: 
            ligne = f.readline().split()

            for step in ligne:
                lecture.append(int(step))

        return lecture

    def build_file(self): 
        """
            Fabrique et sauvegarde la config
        """
        
        with open(self.path, 'w') as f: 

            for i in range(1,self.longueur): 
                f.write(str(randint(0, self.longueur - i)) + " ")

class Dossier:

    def __init__(self):

        self.nombre_qtable = self.nombre_fichiers("qtables")
        self.nombre_config = self.nombre_fichiers("configs")

    
    def nombre_fichiers(self, dossier): #dossier : str, "configs" ou "qtables" 
        """
            Permet de compter le nombre de fichier de config et de qtable dans les dossiers de stockage
        """

        Liste_fichiers = [fichier for fichier in os.listdir(dossier)]
        compteur = 0 

        for i in range(len(Liste_fichiers)) :

            fichier = Liste_fichiers[i]
            
            if dossier == "qtables":
                if fichier[0] == "q" :
                    compteur += 1

            elif dossier == "configs" :
                if fichier[:4] == "conf" :
                    compteur += 1
        
        return compteur