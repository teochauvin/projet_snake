import sys, time, pygame
import os
from pygame.locals import *
from random import *
import numpy as np
from math import sqrt, pow

#######IMPORTANT#######
    # CODE NUMERIQUE
    # 0 1 2 3 ACTIONS
    # 4 FOOD
    # 5 EMPTY
#######################

class Moteur: 

    def __init__(self, taille, config, joueur): 

        self.taille = taille
        self.fichier_config_path = config

        self.plateau = [[5 for _ in range(self.taille)] for _ in range(self.taille)]
        self.plateau[joueur.position_Y][joueur.position_X] = joueur.save_action

        self.score = 0
        self.in_game = True

        self.fruit_X = None
        self.fruit_Y = None

        self.config = []

        # Si la config n'existe pas on la créer puis on la charge
        if os.path.exists(config):
            self.config = self.get_config() 
        else: 
            self.build_config(config, self.taille**2)
            self.config = self.get_config()

        self.add_fruit()

        self.learning_rate = 0.1
        self.gamma = 0.9

        self.Q = [[0 for _ in range (4)] for _ in range(9)]

    def reset(self, joueur): 
        """
            Réinitialisation des variables du plateau 
        """

        self.plateau = [[5 for _ in range(self.taille)] for _ in range(self.taille)]
        self.plateau[joueur.position_Y][joueur.position_X] = joueur.save_action

        self.score = 0
        self.in_game = True

        self.fruit_X = None
        self.fruit_Y = None

        self.config = []

        if os.path.exists( self.fichier_config_path):
            self.config = self.get_config() 
        else: 
            self.build_config( self.fichier_config_path, self.taille**2)
            self.config = self.get_config()

        self.add_fruit()
    
    def get_config(self): 
        """
            Récupère un fichier de config et le sauvegarde
        """

        lecture = [] 

        with open(self.fichier_config_path, 'r') as f: 
            ligne = f.readline().split()

            for step in ligne:
                lecture.append(int(step))

        return lecture

    def build_config(self, path, n_elt): 
        """
            Fabrique un fichier de config avec des évènements aléatoires
        """

        with open(path, 'w') as f: 
            for i in range(n_elt): 
                f.write(str(randint(0, self.taille**2 - i)) + " ")

    def is_snake(self, position): 
        """
            Retourne True si la case est un serpent en mémoire
        """
        block = self.plateau[position[1]][position[0]]

        return block >= 0 and block < 4 

    def is_food(self, position): 
        """
            Retourne True si la case est de la nourriture en mémoire
        """

        return self.plateau[position[1]][position[0]] == 4

    def is_wall(self, position):
        """
            Retourne True si le serpent est en dehors du plateau
        """
        return position[0]<0 or position[0]>=self.taille or position[1]<0 or position[1]>=self.taille

    def update_position(self, joueur): 
        """
            Met à jour la position du joueur en mémoire
        """

        self.plateau[joueur.position_Y][joueur.position_X] = joueur.save_action

        # Future position de la tete
        next_position_X = joueur.position_X + joueur.actions[joueur.save_action][0] 
        next_position_Y = joueur.position_Y + joueur.actions[joueur.save_action][1]

        position = (next_position_X, next_position_Y)
        
        # Si la tête du serpent ne heurte rien, on actualise sa position
        if self.is_wall(position) or self.is_snake(position): 
            self.end_process()

        else: 
            joueur.position_X = next_position_X
            joueur.position_Y = next_position_Y

            
            if self.is_food((joueur.position_X, joueur.position_Y)): 

                self.score += 1
                self.add_fruit()

            # Gestion de l'avencement de la queue du serpent
            else: 
                action_queue = self.plateau[joueur.position_queue_Y][joueur.position_queue_X]

                next_position_queue_X = joueur.position_queue_X + joueur.actions[action_queue][0]
                next_position_queue_Y = joueur.position_queue_Y + joueur.actions[action_queue][1]

                self.plateau[joueur.position_queue_Y][joueur.position_queue_X] = 5

                joueur.position_queue_X = next_position_queue_X
                joueur.position_queue_Y = next_position_queue_Y

    def end_process(self): 
        """
            Fin du jeu, on peut ajouter les sauvegardes ici
        """

        self.in_game = False
        #sys.exit()

    def add_fruit(self):
        """
            Placer le prochain fruit à partir du fichier de config
        """

        count = 0

        for y in range(0, self.taille): 
            for x in range(0, self.taille):
                
                if self.plateau[y][x] == 5:
                    if count == self.config[self.score]:
                        self.plateau[y][x] = 4

                        self.fruit_X = x 
                        self.fruit_Y = y

                    count += 1
        
    def distance_from_fruit(self, case): 
        """
            Donne la distance d'une case au fruit
        """

        return sqrt(pow(case[0] - self.fruit_X, 2) + pow(case[1] - self.fruit_Y, 2)) 

    def get_state(self, next_position_X, next_position_Y): 
        """
            Retourne l'état d'une position pour l'apprentissage par renforcement. Les états sont ici : NO N NE E SE S SO O et le centre.
            Ils correspondent au secteur dans lequel se trouve le fruit par rapport à la tête du serpent. 
        """

        if self.fruit_X == next_position_X: 
            if self.fruit_Y > next_position_Y: 
                state = 4
            elif self.fruit_Y < next_position_Y: 
                state = 0
        if self.fruit_Y == next_position_Y: 
            if self.fruit_X > next_position_X:
                state = 2
            elif self.fruit_X < next_position_X:
                state = 6
        if self.fruit_X > next_position_X and self.fruit_Y > next_position_Y: 
            state = 3
        if self.fruit_X < next_position_X and self.fruit_Y > next_position_Y:
            state = 5
        if self.fruit_X > next_position_X and self.fruit_Y < next_position_Y:
            state = 1
        if self.fruit_X < next_position_X and self.fruit_Y < next_position_Y:
            state = 7
        if self.fruit_X == next_position_X and self.fruit_Y == next_position_Y:
            state = 8

        return state

    def evaluer(self, joueur, at): 
        """
            Associe une récompense à un état donné à un instant t. Renvoie l'état à t + 1 ainsi que la récompense.
            + 1 si le serpent mange le fruit, - 1 si le serpend perd 
        """     

        reward = 0

        next_position_X = joueur.position_X + joueur.actions[at][0] 
        next_position_Y = joueur.position_Y + joueur.actions[at][1] 

        next_pos = (next_position_X, next_position_Y)

        if next_position_X == self.fruit_X and next_position_Y == self.fruit_Y: 
            reward = 1
        elif self.is_wall(next_pos) or self.is_snake(next_pos): 
            reward = -1
        #else: 
        #    reward = 1/(self.distance_from_fruit(next_pos))**2

        state = self.get_state(next_position_X, next_position_Y)

        return state, reward

    def bellman_equation(self, at, atp1, st, stp1, reward): 
        """
            Mise à jour de la Q table à l'aide de l'equation de Bellman
        """

        self.Q[st][at] = self.Q[st][at] + self.learning_rate*(reward + self.gamma*self.Q[stp1][atp1] - self.Q[st][at])

    def save_q(self, path):
        """
            Enregistre la q_table dans path
        """ 
        with open(path, 'w') as f: 
            for i in range(len(self.Q)): 
                f.write("{},{},{},{}\n".format(self.Q[i][0],self.Q[i][1],self.Q[i][2],self.Q[i][3]))

    def load_q(self, path):
        """
            Charge la q_table du fichier path
        """ 

        Q = []

        with open(path, 'r') as f: 
            lignes = f.readlines()

            for ligne in lignes:
                tab = [] 
                for c in ligne.split(","): 
                    tab.append(float(c))

                Q.append(tab)

        return Q


class Affichage: 

    def __init__(self, taille_fenetre, taille_jeu):

        self.taille_fenetre = taille_fenetre
        self.taille_jeu = taille_jeu
        self.bps = taille_fenetre//taille_jeu

        pygame.init()
        self.surface = pygame.display.set_mode((self.taille_fenetre, self.taille_fenetre)) 
        self.FPS = pygame.time.Clock()

    def afficher(self, memoire, score, joueur): 
        """
            Afiche le contenu de la mémoire du moteur de jeu à un instant donné
        """

        pygame.display.update()

        self.surface.fill((0, 0, 0))

        for x in range(self.taille_jeu): 
            for y in range(self.taille_jeu): 

                block = memoire[y][x]

                if block >= 0 and block < 4:
                    pygame.draw.rect(self.surface, (255, 255, 255), (x*self.bps, y*self.bps, self.bps, self.bps))

                if block == 4: 
                    pygame.draw.rect(self.surface, (0, 255, 0), (x*self.bps, y*self.bps, self.bps, self.bps))

        pygame.draw.rect(self.surface, (255, 255, 255), (joueur.position_X*self.bps, joueur.position_Y*self.bps, self.bps, self.bps))

        # Affichage du score 
        font = pygame.font.SysFont("Helvetica", 15)
        text = font.render("Score : " + str(score), True, (255, 255, 255))
        self.surface.blit(text, (420,480))


class Joueur: 

    def __init__(self, position_init): 

        self.position_X = position_init[0] 
        self.position_Y = position_init[1] 

        self.position_queue_X = position_init[0] 
        self.position_queue_Y = position_init[1] 

        self.pos_init_x = position_init[0] 
        self.pos_init_y = position_init[1] 

        # Actions de déplacement
        self.actions = [
            [0,1],
            [1,0],
            [0,-1],
            [-1,0]
        ]  

        self.save_action = 1

        self.nature = None

    def get_nature(self): 
        return self.nature

    def reset(self): 
        """
            Réinitialise les variables de position du joueur pour redémarrer la partie dans les mêmes conditions
        """
        
        self.position_X = self.pos_init_x
        self.position_Y = self.pos_init_y

        self.position_queue_X = self.pos_init_x
        self.position_queue_Y = self.pos_init_y

        self.save_action = 1

class Human(Joueur): 

    def __init__(self, position_init): 
        Joueur.__init__(self, position_init)

        self.nature = "Humain"

    def get_action(self): 
        """
            Retourne l'action entrée par le joueur 
        """

        pressed_keys = pygame.key.get_pressed()

        tmp = self.save_action

        if pressed_keys[K_UP]: 
            tmp = 2
        elif pressed_keys[K_RIGHT]: 
            tmp = 1
        elif pressed_keys[K_DOWN]: 
            tmp = 0
        elif pressed_keys[K_LEFT]: 
            tmp = 3

        # Empêche le retour en arrière du serpent pendant le jeu 
        if not (self.actions[tmp][0] + self.actions[self.save_action][0] == 0 and self.actions[tmp][1] + self.actions[self.save_action][1] == 0):
            self.save_action = tmp
        
        return self.save_action

class Agent(Joueur):

    def __init__(self, position_init):
        Joueur.__init__(self, position_init)

        self.nature = "Agent" 

    def get_action(self, st, Q, eps): 
        """
            Algorithme epsilon-greedy
        """

        tmp = self.save_action

        if uniform(0, 1) < eps: 
            tmp = randint(0, 3)

        else: # Or greedy action 
            tmp = np.argmax(Q[st])

        # Empêche le retour en arrière du serpent pendant le jeu 
        if not (self.actions[tmp][0] + self.actions[self.save_action][0] == 0 and self.actions[tmp][1] + self.actions[self.save_action][1] == 0):
            self.save_action = tmp

        return self.save_action
