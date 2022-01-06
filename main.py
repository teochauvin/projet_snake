import sys, time, pygame
from pygame.locals import *
from modules import *
import pickle
import math

agent = Agent((2,2)) 
moteur = Moteur(20, "configs/conf_1.cf", agent)

def train(n):
    """
    Entrainement de l'agent. Le paramètre n correspond au nombre de partie qu'il jouera
    """
    for k in range(n):

        if k%10000 == 0:
            print(k)
        
        # Remise à zéro du plateau et de l'agent 
        agent.reset()
        moteur.reset(agent)  

        # Etat initial
        st = moteur.get_state(agent.position_X, agent.position_Y)

        while moteur.in_game: 

            # Récupération de l'action que l'agent souhaite réaliser 
            at = agent.get_action(st, moteur.Q, 0.6) 
            #print(at)

            # Evaluation 
            stp1, r = moteur.evaluer(agent, at)
            #print(stp1, r)

            # Meilleure action
            atp1 = agent.get_action(stp1, moteur.Q, 0.0)
            #print(atp1)

            # Actualisation de la Q table
            moteur.bellman_equation(at, atp1, st, stp1, r)

            # Actualisation de la position du joueur 
            moteur.update_position(agent) 

            st = stp1

            #time.sleep(2)

    # Enregistrement de la qtable
    moteur.save_q('q_tables/qtable_1')

def jeu_visuel(human=False): 
    """
    Permet la visualisation du jeu de l'agent après entrainement
    Permet également de lancer le jeu pour un utilisateur
    """
    if human:
        joueur = Human((2,2))
    else: 
        joueur = Agent((2,2)) 

    joueur.reset()
    moteur.reset(joueur)

    # Récupération de la Q table
    Q = moteur.load_q('q_tables/qtable_1')

    affichage = Affichage(500, 20) 

    # Etat initial
    st = moteur.get_state(joueur.position_X, joueur.position_Y)

    while moteur.in_game:

        # On récupère l'action que le joueur / agent veut réaliser
        if not human:
            st = moteur.get_state(joueur.position_X, joueur.position_Y)
            at = joueur.get_action(st, Q, 0.0) 
        else: 
            at = joueur.get_action()

        # Affichage
        affichage.afficher(moteur.plateau, moteur.score, joueur)

        # Actualisation de la position du joueur 
        moteur.update_position(joueur) 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        affichage.FPS.tick(10)
    sys.exit()


# Test

if __name__ == "__main__" :
    train(100) 
    jeu_visuel(human = False)
