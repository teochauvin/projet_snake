from data import *

class Case: 

    def __init__(self, position): 
        """
            Represente une case du plateau de jeu
        """

        self.x = position[0]
        self.y = position[1] 

        self.etat = "Vide"

    def position(self): 
        return (self.x, self.y)

class Snake(Case): 

    def __init__(self, position): 
        """
            Hérite de Case, c'est une case du corps du snake
        """

        Case.__init__(self, position)
        self.etat = "Snake"

class Nourriture(Case): 

    def __init__(self, position):
        """
            Hérite de Case, c'est la nourriture du plateau
        """

        Case.__init__(self, position)
        self.etat = "Nourriture"

    def surNourriture(self, position): 
        """
            Test si la position proposée est celle de la nourriture à l'instant t
        """
        return position[0] == self.x and position[1] == self.y

    def changer_position(self, position):
        """
            Actualise la position de la case nourriture
        """
        self.x = position[0]
        self.y = position[1]

class Snake_corps: 

    def __init__(self, position_initiale): 

        self.corps = [Snake(position_initiale)]

    def tete(self): 
        return self.corps[0] 

    def queue(self): 
        return self.corps[len(self.corps)-1] 

    def bouge_queue(self): 
        """
            Supprime le dernier élément de la liste corps snake
        """
        del self.corps[len(self.corps)-1]

    def bouge_tete(self, position): 
        """
            Insere un nouvel élément en index 0 pour faire bouger la tete à la nouvelle position
        """
        self.corps.insert(0, Snake(position))

    def sur_serpent(self, position):
        """
            Test si la position renseignee est sur le snake
        """

        for case in self.corps: 
            if case.x == position[0] and case.y == position[1]: 
                return True
        return False

    def ProchainePosition(self, mouvement):
        """
            Determine en fonction du mouvement du snake quel sera sa prochaine position
        """

        position_tete = self.tete().position() 

        prochaine_position_x = position_tete[0] + mouvement[0] 
        prochaine_position_y = position_tete[1] + mouvement[1] 

        return (prochaine_position_x, prochaine_position_y)


class Moteur: 

    def __init__(self, taille_mémoire, position_initiale, id_config = 1, id_qtable = 1): 
        """
            Initialise le moteur de jeu, il gere le corps du snake, la position de la nourriture, les mouvements réalisables
        """

        self.taille_memoire = taille_mémoire
        self.position_initiale = position_initiale

        self.snake = Snake_corps(self.position_initiale) 

        self.id_config = id_config
        self.config = self.get_ListePositionNourriture(self.id_config)
        self.liste_position_nourriture = self.config.get()

        self.score = 0
        self.en_jeu = True

        self.nourriture = Nourriture(self.PositionNourritureSuivante())

        self.mouvements_ref_plateau = [
            [0,-1],
            [1,0],
            [0,1], 
            [-1,0]
        ]

    def reinitialiser(self):
        """
            Réinitialiser le moteur permet de relancer une partie sans créer une nouvelle instance de Moteur
        """

        self.snake = Snake_corps(self.position_initiale) 

        self.score = 0
        self.en_jeu = True

        self.liste_position_nourriture = self.config.get()
        self.nourriture = Nourriture(self.PositionNourritureSuivante())

    def get_ListePositionNourriture(self, id=1): 
        """
            Créé un fichier de config (objet), Configs contient une liste des positions des nourritures
        """
        return Configs(self.taille_memoire, id) 

    def PositionNourritureSuivante(self): 
        """
            Algorithme qui determine quel sera la prochaine position de la nourriture d'après ce qu'on peut lire
            dans le fichier de config à l'étape i
        """

        n = self.liste_position_nourriture[self.score] 

        while True:
            compteur = 0
            
            for x in range(self.taille_memoire): 
                for y in range(self.taille_memoire): 

                    if not self.snake.sur_serpent((x,y)):

                        if compteur == n:
                            return (x,y)

                        else:
                            compteur += 1 

            n -= compteur

    def sur_plateau(self, prochaine_position): 
        """
            Test si la position est sur le plateau
        """

        return prochaine_position[0] >= 0 and prochaine_position[0]<self.taille_memoire and prochaine_position[1] >= 0 and prochaine_position[1]<self.taille_memoire

    def mouvement_possible(self, prochaine_position): 
        """
            Test si la position envisagée est sur le plateau et pas sur le snake, donc si le mouvement est libre
        """
        return not self.snake.sur_serpent(prochaine_position) and self.sur_plateau(prochaine_position)
 
    def fin(self): 
        self.en_jeu = False

    def update(self, actionRefPlateau, joueur): 
        """
            Gere le déplacement de la tête et la queue du serpent
            Place un nouveau fruit si besoin en augmantant le score
        """

        joueur.action_ref_plateau = actionRefPlateau

        # donnees
        position_tete = self.snake.tete().position()
        position_queue = self.snake.queue().position()

        # vecteur de déplacement
        mouvement = self.mouvements_ref_plateau[actionRefPlateau]

        # on bouge la tete
        prochaine_position = self.snake.ProchainePosition(mouvement)

        if self.mouvement_possible(prochaine_position):
            self.snake.bouge_tete(prochaine_position)
        else: 
            self.fin()

        # on verifie qu'il mange, si oui on bouge pas la queue 
        if not prochaine_position == self.nourriture.position(): 
            self.snake.bouge_queue()
        else:
            self.nourriture.changer_position(self.PositionNourritureSuivante())
            self.score += 1
