from Card import *

class Hand: #Classe représentant la main d'un joueur

    def __init__(self, expert):

        self.Cards = [] #Liste de cartes contenues dans la main du joueur
        if expert: #Si le mode est expert, la taille maximale de la main est de 7 sinon de 6
            self.MaxSize = 7
        else:
            self.MaxSize = 6
        self.Size = 0 #Taille actuelle de la main

    def fillHand(self, card_draw): #Méthode remplissant la main du joueur à partir d'une pioche donnée

        for i in range(self.MaxSize):
            self.draw(card_draw)

    def draw(self, card_draw): #Méthode ajoutant une carte dans la main du joueur à partir d'une pioche donnée

        self.Cards.append(card_draw.draw())
        self.Size += 1

    def playCard(self, n): #Méthode retournant la n-ième carte de la main du joueur (supprimant également la carte de la liste)

        card = self.Cards.pop(n)
        self.Size -= 1

        return card

    def generateState(self): #Méthode retournant une représentation simplifiée de la main sous forme d'une liste de tuples de deux valeurs

        state_hand = []

        for card in self.Cards: #Pour chaque cartes de la main, on ajoute à notre liste le tuple 
            state_hand.append((card.Value,find_key(COLORS,card.Color)))

        return state_hand

    def __str__(self): #Méthode affichant l'objet (phases de test)

        concat = ""
        n = 1
        for card in self.Cards:
            concat += "{}: ".format(n)
            concat += card.__str__()
            concat += "  "
            n += 1
        concat += "\n"

        return concat
        