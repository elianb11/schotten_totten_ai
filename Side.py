from Card import *

class Side: #Classe représentant le côté d'une frontière

    def __init__(self):

        self.Cards = [] #Liste des cartes posées
        self.MaxSize = 3 #Maximum de cartes pouvant être posées
        self.Size = 0 #Nombre de cartes posées
        self.Power = 0 #Puissance de la combinaison de cartes posées (initialisé à 0)
        self.Sum = 0 #Somme de la combinaison des cartes posées (initialisé à 0)

    def isFull(self): #Méthode retournant si la liste est de taille maximale ou non

        return (self.MaxSize == self.Size)

    def isEmpty(self): #Méthode retournant si la liste est vide ou non

        return (self.Size == 0)

    def addCard(self, card): #Méthode ajoutant une carte donnée à la liste de cartes posées

        if not (self.isFull()): #Si la liste n'est pas encore de taille maximale...
            self.Cards.append(card)
            self.Size += 1
        else:
            print("This is full !")

    def computePowerAndSum(self): #Fonction actualisant les attributs Power et Sum

        if (self.isFull()):
            self.Power = computePower(self.Cards) #On calcule la puissance de la combinaison
            self.Sum = computeSum(self.Cards) #On calcule la somme de la combinaison

    def __str__(self): #Méthode affichant l'objet (phases de test)

        concat = ""
        for card in self.Cards:
            concat += card.__str__()
            concat += " "
        for i in range(self.MaxSize - self.Size):
            concat += "|      _      | "
        return concat