import sys, time, pygame
from pygame.locals import *

from moteur import *

class Affichage: 

    def __init__(self, ppb, moteur):
        """
            On appelle le moteur pour definir l'affichage pour avoir accès aux variables qui définissent la forme du jeu
            On initialise pygame
        """

        self.ppb = ppb
        self.taille_memoire = moteur.taille_memoire
        self.taille_fenetre = self.taille_memoire*self.ppb

        pygame.init()
        self.surface = pygame.display.set_mode((self.taille_fenetre, self.taille_fenetre)) 
        self.FPS = pygame.time.Clock()

    def afficher(self, moteur): 
        """
            Afficher se contente de demander au snake sur quelles cases il est puis de les afficher
            De même pour la nourriture
            Le reste du plateau n'est pas traité par l'affichage
            On affiche le score en bas à droite
        """

        pygame.display.update()
        self.surface.fill((0, 0, 0))

        # Snake
        for case in moteur.snake.corps: 
            pygame.draw.rect(self.surface, (255, 255, 255), (case.x*self.ppb, case.y*self.ppb, self.ppb, self.ppb))

        # Nourriture
        nourriture = moteur.nourriture
        pygame.draw.rect(self.surface, (0, 255, 0), (nourriture.x*self.ppb, nourriture.y*self.ppb, self.ppb, self.ppb))

        # Score 
        font = pygame.font.SysFont("Helvetica", 15)
        text = font.render("Score : " + str(moteur.score), True, (255, 255, 255))
        self.surface.blit(text, (520,580))