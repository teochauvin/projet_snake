from data import *
from math import *

class Entraineur: 

    def __init__(self, id_qtable=1, learningRate = 0.1, gamma=0.9): 
        """
            Initialise une QTable, l'entraineur est la classe qui fait la liaison avec le QLearning
        """

        self.QTable = QTable(id_qtable) 

        self.learningRate = learningRate
        self.gamma = gamma


    def VecteurVersNourriture(self, position, moteur):
        """
            Retourne un delta_x, delta_y dans le référentiel du plateau qui indique la position relative de la nourriture
        """ 

        position_nourriture = moteur.nourriture.position()
        position_tete = position

        deltaX = position_nourriture[0] - position_tete[0]
        deltaY = position_nourriture[1] - position_tete[1] 

        return (deltaX, deltaY)

    def ReferentielPlateauASnake(self, delta, joueur): 
        """
            Permet de convertir la position relative de la nourriture dans le référentiel plateau au référentiel snake
        """

        directionRefPlateau = joueur.action_ref_plateau

        delta_x = delta[0]
        delta_y = delta[1]

        f,r = 0,0

        # bas, droite, haut, gauche
        # on passe dans le referentiel du serpent
        if directionRefPlateau == 0: 
            f = -delta_y
            r = delta_x
        if directionRefPlateau == 1: 
            f = delta_x
            r = delta_y
        if directionRefPlateau == 2: 
            f = delta_y
            r = -delta_x
        if directionRefPlateau == 3: 
            f = -delta_x
            r = -delta_y

        return (f,r)

    def get_Etat(self, position, moteur, joueur):
        """
            Regarde dans quel cadrant se situe la nourriture par rapport à la direction de déplacement du snake
            Regarde également le danger présent sur les cases adjacentes
            Permet de retourner un état entre 0 et 63
        """

        etat = None 

        deltaRefPlateau = self.VecteurVersNourriture(position, moteur)

        deltaRefSnake = self.ReferentielPlateauASnake(deltaRefPlateau, joueur)
        f,r = deltaRefSnake

        if f>0: 
            # Devant à droite
            if r>0: 
                etat = 3
            # Devant à gauche
            if r<0: 
                etat = 5
            # Devant en face
            if r==0: 
                etat = 4
        elif f<0: 
            # Derierre à droite
            if r>0: 
                etat = 1
            # Derierre à gauche
            if r<0: 
                etat = 7
            # Derierre 
            if r==0: 
                etat = 0
        elif f==0: 
            # a droite
            if r>0: 
                etat = 2
            # a gauche
            if r<0: 
                etat = 6
            if r==0: 
                etat = 4

        dangers_index = 0
        for i in range(-1, 2, 1): 

            x,y = moteur.snake.tete().position()
            
            X = x + moteur.mouvements_ref_plateau[joueur.ReferentielSnakeAPlateau(i)][0]
            Y = y + moteur.mouvements_ref_plateau[joueur.ReferentielSnakeAPlateau(i)][1]

            position = (X,Y)

            if not moteur.sur_plateau(position) or moteur.snake.sur_serpent(position): 
                dangers_index += 2**(i+1)

        return etat*8 + dangers_index

    def Rapprochement(self, positionNourriture, position, prochainePosition): 
        """
            Retourne true si la variation de position relative par rapport à la nourriture diminue
        """

        if abs(prochainePosition[0] - positionNourriture[0]) < abs(position[0] - positionNourriture[0]):
            return True
        elif abs(prochainePosition[1] - positionNourriture[1]) < abs(position[1] - positionNourriture[1]):
            return True
        else: 
            return False

    def EvaluerPosition(self, actionReferentielPlateau, moteur, joueur): 
        """
            La stratégie d'apprentissage est en partie orientée par le système de récompenses géré ici
        """

        recompense = 0 

        mouvement = moteur.mouvements_ref_plateau[actionReferentielPlateau]
        prochaine_position = moteur.snake.ProchainePosition(mouvement)

        if moteur.nourriture.surNourriture(prochaine_position):
            recompense = 10

        if self.Rapprochement(moteur.nourriture.position(), moteur.snake.tete().position(), moteur.snake.ProchainePosition(mouvement)):
            recompense = 1
        else: 
            recompense = -1
        
        if moteur.snake.sur_serpent(prochaine_position) or not moteur.sur_plateau(prochaine_position): 
            recompense = -10


        etat = self.get_Etat(prochaine_position, moteur, joueur)

        return etat, recompense

    def ActualiserQTable(self, action, actionSuivant, etat, etatSuivant, recompense):
        """
            On applique la formule définie par récurence de Bellman pour actualiser la QTable
            Gamma correspond au poids qu'on souhaite donner aux actions futures dans la décision d'une action instantanée
            Alpha, le leraning rate correspond à "l'agressivité" du snake, son inertie 
        """

        self.QTable.Q[etat][action] = self.QTable.Q[etat][action] + self.learningRate*(recompense + self.gamma*self.QTable.Q[etatSuivant][actionSuivant] - self.QTable.Q[etat][action])

