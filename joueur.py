from tkinter import NE
import pygame
from moteur import *
from random import *
import numpy as np

class Joueur: 

    def __init__(self): 

        self.action_ref_plateau = 1

    def get_InterractionHumaine(self): 
        """
            Permet de récupérer les actions effectuées par un humain
        """

        self.action_ref_plateau = self.clavier() 
        return self.action_ref_plateau

    def clavier(self):
        """
            Utilise la programmation concurrentielle. On interroge périodiquement la boucle autonome qui gère les évents python
            et nous récupérons une liste des actions effectuée. On traite la liste de sorte à ne garder que l'événement 
            intéressant le plus récent possible
        """ 

        events = pygame.event.get()
        for i in range(len(events)): 
                
            e = events.pop()

            # c'est une touche
            if e.type == pygame.KEYDOWN: 

                if e.key == pygame.K_UP:
                    return 0
                elif e.key == pygame.K_RIGHT:
                    return 1
                elif e.key == pygame.K_DOWN:
                    return 2
                elif e.key == pygame.K_LEFT:
                    return 3

        return self.action_ref_plateau

    def VarEpsilon(self, nEpochs, rank): 
        """
            Donne la possibilité de faire varier epsilon, ici il est fixe.
            p correspond au pourcentage de l'apprentissage
        """
        p = rank/nEpochs
        
        return 0.8
            
    def EpsilonGreedy(self, etat, Qtable, eps): 
        """
            Algorithme epsilon-greedy qui permet de réaliser de l'exploration et de l'exploitation de l'nvironnement
        """

        if uniform(0, 1) < eps: 
            action = randint(0, 2)

        else: 
            action = np.argmax(Qtable.Q[etat])
        
        return action   

    def MeilleureAction(self, etat, Qtable):
        """
            Exploitation pure de la QTable
        """
        return self.EpsilonGreedy(etat, Qtable, 0.0)

    def ReferentielSnakeAPlateau(self, action): 
        """
            Permet de passer du referentiel snake à celui du plateau
        """
        
        arp = self.action_ref_plateau
        arp = (arp + action -1)%4
        return arp
