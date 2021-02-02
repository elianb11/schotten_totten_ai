import copy
import pygame

SUITE_COLOR = 4
BRELAN = 3
COLOR = 2
SUITE = 1

def nextState(player, s): #Fonction renvoyant une liste des prochains états d'un état donné pour le tour du joueur ayant connaissance de sa main

    s_hand = s[0] #La première partie de l'état correspond à la main
    s_board = s[1] #La deuxième au plateau

    next_states = []

    frontierToConsider = frontierToConsider(player, s)

    for card in range(0,len(s_hand)): #Pour chaque cartes de la main du joueur...
        for frontier in range(0,9): #Pour chaque frontières...

            new_s = copy.deepcopy(s) #On créé une copie profonde de l'état car en Python les listes sont des objets et s n'est donc qu'un pointeur
            new_s_hand = new_s[0]
            new_s_board = new_s[1]

            if  s_board[frontier][3+player*3] == (0,0) and s_board[frontier][0] == -1: #Si la côté de la frontière n'est pas complet et que la frontière n'est pas revendiquée

                i = 1
                while s_board[frontier][i+player*3] != (0,0): #On se positionne sur le premier emplacement vide
                    i+=1
                new_s_board[frontier][i+player*3] = new_s_hand.pop(card) #On y ajoute la carte en question
                
                frontier_to_claim = [] #On créé une liste de frontière à revendiquée

                for frontier2 in range(0,9):
                    if claim_ai(player, new_s_board[frontier2], unrevealedCards_ai(new_s_board)): #Si la frontière en question est revendicable, on ajoute son numéro à la liste
                        frontier_to_claim.append(frontier2)

                next_states.append((new_s, card, frontier, frontier_to_claim)) #On ajoute à la liste un tuple composé d'un nouvel état, le numéro de la carte et de la frontière a sélectionnée pour arriver à cet état et la liste des frontières à revendiquées

    return next_states


def nextStateOpponent(player, s): #Fonction renvoyant une liste des prochains états d'un état donné pour le dtour de l'adversaire


    bestPotentialHand = bestPotentialHand(unknownCards_ai(s))

    if player:
        opponent = 0
    else:
        opponent = 1

    s_board = s[1]

    next_states = []

    for card in range(0,len(bestPotentialHand)): #Pour chaque cartes des 6 meilleurs possibles...
        for frontier in range(0,9): #Pour chaque frontières...

            new_s = copy.deepcopy(s) #On créé une copie profonde de l'état
            new_s_board = new_s[1]

            if  s_board[frontier][3+opponent*3] == (0,0) and s_board[frontier][0] == -1: #Si la côté de la frontière n'est pas complet et que la frontière n'est pas revendiquée

                i = 1
                while s_board[frontier][i+opponent*3] != (0,0): #On se positionne sur le premier emplacement vide
                    i+=1
                new_s_board[frontier][i+opponent*3] = bestPotentialHand[card] #On y ajoute la carte en question
                
                frontier_to_claim = [] #On créé une liste de frontière à revendiquée

                for frontier2 in range(0,9):
                    if claim_ai(opponent, new_s_board[frontier2], unrevealedCards_ai(new_s_board)): #Si la frontière en question est revendicable, on ajoute son numéro à la liste
                        frontier_to_claim.append(frontier2)

                next_states.append((new_s, card, frontier, frontier_to_claim)) #On ajoute à la liste un tuple composé d'un nouvel état, le numéro de la carte et de la frontière a sélectionnée pour arriver à cet état et la liste des frontières à revendiquées

    return next_states


def bestPotentialHand(unknownCards): #Fonction qui retourne les 6 meilleures cartes encore non-révélées du jeu

    unknownCards.sort()

    bestPotentialHand = []

    for i in range(0,6):
        bestPotentialHand.append(unknownCards[i])

    return bestPotentialHand
    

def frontierToConsider(player,s):

    return 1


def unrevealedCards_ai(board): #Fonction qui retourne la liste des cartes encore non-révélées du jeu

    unrevealedCards = []

    for i in range(1,10):
        for j in range(1,7):

            unrevealedCards.append((i,j)) #On ajoute dans une liste toutes les cartes du jeu

    for i in range(0,9):
        for j in range(1,7):

            if board[i][j] != (0,0):
                unrevealedCards.remove(board[i][j]) #On supprime celles deja posées sur le plateau 

    return unrevealedCards

        
def unknownCards_ai(s): #Fonction qui retourne la liste des cartes que le joueur n'a pas encore rencontré (carte de la main adverse + pioche)

    unknownCards = []

    for i in range(1,10):
        for j in range(1,7):

            unknownCards.append((i,j)) #On ajoute à la liste toutes les cartes du jeu

    hand = s[0]

    board = s[1]

    for card in hand:
        unknownCards.remove(card) #On supprime toute celles contenues dans la main du joueur

    for i in range(0,9):
        for j in range(1,7):

            if board[i][j] != (0,0):
                unknownCards.remove(board[i][j]) #On supprime celles deja posées sur le plateau 

    return unknownCards

def claim_ai(player, frontier, unrevealedCards): #Version "état simplifié" de la fonction claim (voir Frontier.py)

        if (frontier[3+player*3] != (0,0) and frontier[0] == -1):
            if (frontier[3] == (0,0) and frontier[6] == (0,0)):
                canBeClaimed = isStronger_ai(player,frontier)
            else:
                canBeClaimed = cantBeStrongerThan_ai(player, frontier, unrevealedCards)
        else:
            canBeClaimed = False

        return canBeClaimed

def isStronger_ai(player, frontier): #Version "état simplifié" de la fonction isStronger (voir Frontier.py)

    side = [[],[]]

    for i in range(1,4):
        side[0].append(frontier[i])
    for i in range(4,7):
        side[1].append(frontier[i])
        
    if (computePower_ai(side[0]) > computePower_ai(side[1])):
        strongest = 0
    if (computePower_ai(side[0]) < computePower_ai(side[1])):
        strongest = 1
    if (computePower_ai(side[0]) == computePower_ai(side[1])):
        if (computeSum_ai(side[0]) > computeSum_ai(side[1])):
            strongest = 0
        if (computeSum_ai(side[0]) < computeSum_ai(side[1])):
            strongest = 1
        if (computeSum_ai(side[0]) == computeSum_ai(side[1])):
            strongest = player

    if strongest == player:
        return True
    else:
        return False

def cantBeStrongerThan_ai(player, frontier, unrevealedCards): #Version "état simplifié" de la fonction cantBeStrongerThan (voir Frontier.py)

    cantBeStronger = True

    side = [[],[]]

    for i in range(1,4):
        side[0].append(frontier[i])
    for i in range(4,7):
        side[1].append(frontier[i])

    if (player):
        opponent = 0
    else:
        opponent = 1

    potentialCards = []

    i=0
    while side[opponent][i] != (0,0) and i < 3:
        potentialCards.append(side[opponent][i])

    powerToBeat = computePower_ai(side[player])
    sumToBeat = computeSum_ai(side[player])

    for card1 in unrevealedCards:
        potentialCards.append(card1)
        if side[opponent][1] == (0,0):
            for card2 in unrevealedCards:
                if card1 == card2:
                    continue
                else:
                    potentialCards.append(card2)
                if side[opponent][0] == (0,0):
                    for card3 in unrevealedCards:
                        if card3 == card1 or card3 == card2:
                            continue
                        else:
                            potentialCards.append(card3)
                        if computePower_ai(potentialCards) > powerToBeat:
                            cantBeStronger = False
                        elif computePower_ai(potentialCards) == powerToBeat and computeSum_ai(potentialCards) > sumToBeat:
                            cantBeStronger = False

                        if (not (cantBeStronger)):
                            break

                        potentialCards.remove(card3)

                if computePower_ai(potentialCards) > powerToBeat:
                    cantBeStronger = False
                elif computePower_ai(potentialCards) == powerToBeat and computeSum_ai(potentialCards) > sumToBeat:
                    cantBeStronger = False

                if (not (cantBeStronger)):
                    break

                potentialCards.remove(card2)

        if computePower_ai(potentialCards) > powerToBeat:
            cantBeStronger = False
        elif computePower_ai(potentialCards) == powerToBeat and computeSum_ai(potentialCards) > sumToBeat:
            cantBeStronger = False

        if (not (cantBeStronger)):
            break

        potentialCards.remove(card1)

    return cantBeStronger

def computePower_ai(Cards): #Version "état simplifié" de la fonction computePower (voir Frontier.py)

    power = 0

    if (isSuite_ai(Cards) and isColor_ai(Cards)):
        power = SUITE_COLOR
    else:
        if (isBrelan_ai(Cards)):
            power = BRELAN
        if (isColor_ai(Cards)):
            power = COLOR
        if (isSuite_ai(Cards)):
            power = SUITE

    return power


def computeSum_ai(Cards): #Version "état simplifié" de la fonction computeSum (voir Frontier.py)

    sum = 0
    for card in Cards:
        sum += card[0]

    return sum


def isColor_ai(Cards): #Version "état simplifié" de la fonction isColor (voir Frontier.py)

    isColor = True
    color_number = Cards[0][1]

    for card in Cards:
        if card[1] != color_number:
            isColor = False
            break

    return isColor


def isBrelan_ai(Cards): #Version "état simplifié" de la fonction isBrelan (voir Frontier.py)

    isBrelan = True
    value = Cards[0][0]

    for card in Cards:
        if card[0] != value:
            isBrelan = False
            break

    return isBrelan


def isSuite_ai(Cards): #Version "état simplifié" de la fonction isSuite (voir Frontier.py)

    suite = True

    list_values = []
    for card in Cards:
        list_values.append(card[0])

    list_values.sort()

    firstValue = list_values.pop(0)
    n = 1
    for i in list_values:        
        if i != firstValue + n:
            suite = False
        n+=1

    return suite