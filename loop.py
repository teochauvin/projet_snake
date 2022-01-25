from tkinter.constants import E
from moteur import *
from joueur import *
from affichage import *
from entraineur import *
from data import *
import matplotlib.pyplot as plt


class Loop: 

    def __init__(self): 

        self.param = None

    def JouerHumain(self): 
        """
            Boucle de jeu d'un humain
            Récupération des actions/Calcul du prochain état/Affichage
        """

        moteur = Moteur(30, (2,2))
        joueur = Joueur()
        affichage = Affichage(20, moteur)

        while moteur.en_jeu:
            
            action = joueur.get_InterractionHumaine()

            moteur.update(action, joueur)

            affichage.afficher(moteur)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            affichage.FPS.tick(10)
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def DemonstrationAgent(self, id_config, id_qtable):
        """
            Fonctionne comme une boucle d'entrainement mais on se contente de lire la qtable sans jamais la modifier
            Exploitation pure de la qtable
        """

        moteur = Moteur(30, (2,2), id_config)
        joueur = Joueur()
        entraineur = Entraineur(id_qtable) 
        affichage = Affichage(20, moteur)

        etat = entraineur.get_Etat(moteur.snake.tete().position(), moteur, joueur) 

        while moteur.en_jeu:

            etat = entraineur.get_Etat(moteur.snake.tete().position(), moteur, joueur) 

            action = joueur.MeilleureAction(etat, entraineur.QTable)

            moteur.update(joueur.ReferentielSnakeAPlateau(action), joueur)

            affichage.afficher(moteur)

            for event in pygame.event.get():
                if event.type == QUIT:
                    moteur.en_jeu = False

            affichage.FPS.tick(60)

        pygame.quit()

    def EntrainerNCycle(self, nCycle, idEpoch, Nepochs, detailler=False, id_qtable = 1): 
        """
            Methode qui permet d'entrainer un agent sur une config pendant N parties 
            Cette méthode correspond à une epoch d'entrainement
        """

        moteur = Moteur(30, (2,2), idEpoch)
        joueur = Joueur()
        entraineur = Entraineur(id_qtable)

        scores = [] 
        eps = joueur.VarEpsilon(Nepochs, idEpoch)

        for k in range(nCycle):

            moteur.reinitialiser()

            etat = entraineur.get_Etat(moteur.snake.tete().position(), moteur, joueur) 

            while moteur.en_jeu:
                
                action = joueur.EpsilonGreedy(etat, entraineur.QTable,eps)

                etatSuivant, recompense = entraineur.EvaluerPosition(joueur.ReferentielSnakeAPlateau(action), moteur, joueur)

                actionSuivant = joueur.MeilleureAction(etat, entraineur.QTable)

                entraineur.ActualiserQTable(action, actionSuivant, etat, etatSuivant, recompense)
                
                action_rp = joueur.ReferentielSnakeAPlateau(action)
                moteur.update(action_rp, joueur)

                etat = etatSuivant

            scores.append(moteur.score)

        entraineur.QTable.get_DetailsQTable()

        if detailler: 
            
            print("Parties effectuées avec la config : {}".format(moteur.config.path))
            print("On sauvegarde la Qtable dans q_{}".format(entraineur.QTable.path))
            print("score moyen : {}".format(sum(scores)/len(scores)))
            print("Valeur de epsilon : {}".format(eps))
        
        entraineur.QTable.SauvegardeQTable()

        return sum(scores)/len(scores)

    def ProgrammeEntrainement(self, epochs, cycleParEpochs, detailler=True, id_qtable = 1, id_config = 1):
        """
            Permet d'ajuster le nombre de cycle et d'époques, de montrer les performances de l'agent à intervalle 
            régulier et peut afficher des performances
        """

        def moyenne_lisee(liste, N):
            somme = np.cumsum(liste)
            somme[N:] = somme[N:]-somme[:-N]
            return [i for i in range(len(somme)-N+1)], somme[N-1:]/N 

        scores_moyens = [] 
        epochs_liste = [i for i in range(epochs)]

        for i in range(epochs): 

            resultat = self.EntrainerNCycle(cycleParEpochs, i, epochs, False, id_qtable) 
            scores_moyens.append(resultat)

            self.DemonstrationAgent(id_config, id_qtable)

        plt.plot(epochs_liste, moyenne_lisee(scores_moyens))
        plt.show()

        sys.exit()


