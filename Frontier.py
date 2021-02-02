from Side import *
from Card import *


class Frontier: #Classe représentant une frontière du plateau

    def __init__(self, number):

        self.Status = -1 #Entier représentant le statut de la frontière (-1 = neutre, 0 = appartient au joueur 1, 1 = appartient au joueur 2)
        self.SpecialEffect = 0 #Effet spécial activé sur la frontière
        self.Side = [Side(), Side()] #Liste contenant les deux objets "Side" associé à la frontière (Side[0] = cartes du joueur 1, Side[1] = cartes du joueur 2)
    

    def claim(self, player, unrevealedCards): #Méthode déterminant si la frontière peut être revendiquée et renvoyant le message adéquat

        if (self.Side[player].isFull()): #Si revendiquant la frontière a posé toutes ses cartes...
            if (self.Side[0].isFull() and self.Side[1].isFull()): #Si les deux joueurs ont posées toutes leurs cartes...
                canBeClaimed = self.isStronger(player) #On vérifie si sa combinaison est plus forte que celle de son adversaire
            else:
                canBeClaimed = self.cantBeStrongerThan(player, unrevealedCards) #Sinon on vérifie que l'adversaire n'a aucun moyen d'avoir une combinaison plus forte
        else:
            canBeClaimed = False

        if (canBeClaimed):
            print("Born has been claimed !")
            message = "Born has been claimed !"
            self.Status = player
        else:
            print("Born can't be claimed ")
            message = "Born can't be claimed !"

        return message

    def isStronger(self, player): #Méthode renvoyant si la combinaison du joueur est plus forte que celle adverse ou non

        self.Side[0].computePowerAndSum() #On calcule les puissances et les sommes des combinaisons des deux côtés de la frontière
        self.Side[1].computePowerAndSum()
        if (self.Side[0].Power > self.Side[1].Power): #On compare dans un premier temps les puissances
            strongest = 0
        if (self.Side[0].Power < self.Side[1].Power):
            strongest = 1
        if (self.Side[0].Power == self.Side[1].Power): #On compare ensuite les sommes en cas d'égalité
            if (self.Side[0].Sum > self.Side[1].Sum):
                strongest = 0
            if (self.Side[0].Sum < self.Side[1].Sum):
                strongest = 1
            if (self.Side[0].Sum == self.Side[1].Sum):
                strongest = player

        if strongest == player: #Si la combinaison la plus forte est celle du joueur ayant effectué la revendication
            return True
        else:
            return False

    def cantBeStrongerThan(self, player, unrevealedCards): #Méthode renvoyant si la combinaison du joueur ne pourra pas être battu par une autre combinaison adverse

        cantBeStronger = True

        self.Side[player].computePowerAndSum() #On calcule la puissance et la somme de la combinaison du joueur ayant effectué la revendication

        if (player):
            opponent = 0
        else:
            opponent = 1

        potentialCards = [] #On créé une liste de combinaisons encore réalisables par l'adversaire
        for i in range(0, self.Side[opponent].Size):
            potentialCards.append(self.Side[opponent].Cards[i]) #On y ajoute les cartes déjà posées

        powerToBeat = self.Side[player].Power #Puissance à battre
        sumToBeat = self.Side[player].Sum #Somme à battre

        for card1 in unrevealedCards: #Pour chaque cartes non-révélées
            potentialCards.append(card1) #On l'ajoute à la combinaison à tester
            if self.Side[opponent].Size < 2: #Si la combinaison n'est toujours pas complète
                for card2 in unrevealedCards: #Pour chaque cartes non-révélées
                    if card1 == card2: #Si elle est différente de la première carte ajoutée (on évite de créer des doublons)
                        continue
                    else:
                        potentialCards.append(card2) #On l'ajoute à la combinaison à tester
                    if self.Side[opponent].Size < 1: #Si la combinaison n'est toujours pas complète
                        for card3 in unrevealedCards: #Pour chaque cartes non-révélées
                            if card3 == card1 or card3 == card2: #Si elle est différente de la première et la deuxième carte ajoutée (on évite de créer des doublons)
                                continue
                            else:
                                potentialCards.append(card3) #On l'ajoute à la combinaison à tester
                            if computePower(potentialCards) > powerToBeat: #Si la combinaison actuelle est plus forte, on renvoi faux.
                                cantBeStronger = False
                            elif computePower(potentialCards) == powerToBeat and computeSum(potentialCards) > sumToBeat:
                                cantBeStronger = False

                            if (not (cantBeStronger)): #Si on a déjà trouvé un contre exemple, on peut arrêter de boucler
                                break

                            potentialCards.remove(card3) #On supprime la carte de la liste

                    if computePower(potentialCards) > powerToBeat: #Même démarche 
                        cantBeStronger = False
                    elif computePower(potentialCards) == powerToBeat and computeSum(potentialCards) > sumToBeat:
                        cantBeStronger = False

                    if (not (cantBeStronger)):
                        break

                    potentialCards.remove(card2)

            if computePower(potentialCards) > powerToBeat: #Même démarche
                cantBeStronger = False
            elif computePower(potentialCards) == powerToBeat and computeSum(potentialCards) > sumToBeat:
                cantBeStronger = False

            if (not (cantBeStronger)):
                break

            potentialCards.remove(card1)

        return cantBeStronger

    def generateState(self): #Méthode renvoyant le forme simplifié de la frontière sous forme d'une liste composée de la valeur du statut en tête et de tuples associés aux cartes de part et d'autre de la frontière

        state_frontier = []
        state_frontier.append(self.Status)#On ajoute la valeur du statut à la liste

        n=0
        for card in self.Side[0].Cards: #Pour chaque cartes posées du côté 1, on l'ajoute à la liste 
            state_frontier.append((card.Value,find_key(COLORS,card.Color)))
            n+=1
        for empty_slot in range(0,3-n): #Pour chaque cases encore vides, on ajoute le tuple (0,0) à la liste
            state_frontier.append((0,0))

        n=0
        for card in self.Side[1].Cards: #Pour chaque cartes posées du côté 2, on l'ajoute à la liste
            state_frontier.append((card.Value,find_key(COLORS,card.Color)))
            n+=1
        for empty_slot in range(0,3-n): #Pour chaque cases encore vides, on ajoute le tuple (0,0) à la liste
            state_frontier.append((0,0))

        return state_frontier

    def __str__(self): #Méthode affichant l'objet (phases de test)

        concat = self.Side[0].__str__()
        concat += "     <> FRONTIER {}   STATUS {} <>     ".format(
            self.Number, self.Status)
        concat += self.Side[1].__str__()
        concat += "\n"

        return concat