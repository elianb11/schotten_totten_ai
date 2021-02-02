import Card
import random

class Player(): #Classe représentant un joueur

    def __init__(self, name, number, gameboard, hand):

        self.number = number #Numéro du joueur (0 ou 1)
        self.name = name #Nom du joueur
        self.Gameboard = gameboard #Plateau de jeu associé à la partie du joueur
        self.Hand = hand #Main du joueur

    def draw(self): #Méthode faisant piocher le joueur à partir de la pioche séléctionnée

        if (self.Gameboard.ExpertMode):
            selectedDraw = ""
            while selectedDraw != "c" and selectedDraw != "t":
                selectedDraw = input(
                    "Quelle type de carte voulez-vous piocher ? (enter 'c' for 'Clan', enter 't' for 'Tactic')\n")
            if selectedDraw == 'c':
                self.Hand.draw(self.Gameboard.ClanCardDraw)
            else:
                self.Hand.draw(self.Gameboard.TacticCardDraw)
        else:
            self.Hand.draw(self.Gameboard.ClanCardDraw)

    def playTroop(self, nCard, nFrontier): #Méthode pour jouer la carte clan séléctionnée sur une frontière séléctionnée

        self.Gameboard.frontiers[(nFrontier)].Side[(self.number)].addCard(self.Hand.playCard(nCard))

    def claimFrontier(self, frontier_number): #Méthode pour revendiquer une frontière séléctionnée

       return self.Gameboard.frontiers[frontier_number].claim(self.number, self.Gameboard.unrevealedCards())
