import copy
from NextState import *
import random
import time

W1 = 0.2 #Poids des différentes fonctions d'évaluation
W2 = 0.2
W3 = 0.2
W4 = 0.4

def computeNumberFrontier(player, s): #Fonction qui retourne le nombre de frontières revendiquées par un joueur donné

    nb = 0

    for frontier in s[1]:
        if frontier[0] == player:
            nb += 1

    return nb

def eval1(player, s): #Première fonction d'évaluation prenant en compte le nombre de frontières revendiquées

    if player:
        opponent = 0
    else:
        opponent = 1

    nbClaimedFrontier = computeNumberFrontier(player, s) #On calcule le nombre de frontière détenues par la joueur
    nbClaimedFrontierOpponent = computeNumberFrontier(opponent, s) #On calcule le nombre de frontière détenues par son adversaire

    nbMaxClaimedFrontier = 4 #Le nombre maximum de frontière revendiquées avant la victoire

    return (nbClaimedFrontier-nbClaimedFrontierOpponent)/nbMaxClaimedFrontier #Résultat entre -1 et 1

def computeNumberWinningIssue(player, s): #Fonction qui calcule le nombre de possibilités de victoire différentes

    nb = 0
    counter = 0

    for frontier in s[1]: #pour chaque frontières...
        if frontier[0] == player or frontier[0] == -1: #Si on le frontière est neutre ou détenue par le joueur, on incrémente de 1 notre compteur
            counter += 1
        else:
            counter = 0
        if counter >= 3: #Si le compteur atteint 3, on incrémente de 1 le nombre de possibilités de victoire
            nb += 1

    return nb

def eval2(player, s): #Deuxième fonction d'évaluation prenant en compte le nombre de possibilités de victoire différentes

    if player:
        opponent = 0
    else:
        opponent = 1

    nbWinningIssue = computeNumberWinningIssue(player, s) #On calcule le nombre de possibilités de victoire différentes du joueur
    nbWinningIssueOpponent = computeNumberWinningIssue(opponent, s) #On calcule le nombre de possibilités de victoire différentes de son adversaire

    nbMaxWinningIssue = 7 #Le nombre maximum de possibilités de victoire

    return (nbWinningIssue-nbWinningIssueOpponent)/nbMaxWinningIssue #Résultat entre -1 et 1

def computeNumberOneLeftWinningIssue(player, s):#Fonction qui calcule le nombre de séries de 3 frontières adjacentes bientôt achevées

    nb = 0
    counter = 0

    for i in range(0,7): #Pour chaque frontière...
        for j in range(0,3): #Pour la frontière en question et les 2 suivantes...

            if s[1][i+j][0] == -1 or s[1][i+j][0] == player: #On compte le nombre de frontière revnediquées
                if s[1][i+j][0] == player:
                    counter += 1
            else:
                counter = 0 #On descend le compteur à 0 si une frontière de la série est revendiquée par l'adversaire
        
        if counter == 2: #S'il y a exactement deux frontières revendiquées dans la série, on incrémente de 1 notre compteur.
            nb += 1

    return nb

def eval3(player, s): #Troisième fonction d'évaluation qui prend en compte le nombre de séries de 3 frontières adjacentes bientôt achevées

    if player:
        opponent = 0
    else:
        opponent = 1

    nbOneLeftWinningIssue = computeNumberOneLeftWinningIssue(player, s) #On calcule le nombre de séries de 3 frontières adjacentes bientôt achevées par le joueur
    nbOneLeftWinningIssueOpponent = computeNumberOneLeftWinningIssue(opponent, s) #On calcule le nombre de séries de 3 frontières adjacentes bientôt achevées par l'adversaire

    nbMaxOneLeftWinningIssue = 4 #Nombre maximum de série de frontières revendiuées bientôt achevées

    return (nbOneLeftWinningIssue-nbOneLeftWinningIssueOpponent)/nbMaxOneLeftWinningIssue #Résultat entre -1 et 1


def bestPotentialScore(side,unrevealedCards): #Fonction qui retourne le meilleur score potentiel qu'on puisse obtenir sachant les cartes qui n'ont pas encore été révélées

    bestPotentialScore = 0

    for card1 in unrevealedCards: #Pour chaque cartes non-révélées
        side.append(card1) #On l'ajoute à la combinaison à tester
        if side[1] == (0,0): #Si la combinaison n'est toujours pas complète
            for card2 in unrevealedCards: #Pour chaque cartes non-révélées
                if card1 == card2: #Si elle est différente de la première carte ajoutée (on évite de créer des doublons)
                    continue
                else:
                    side.append(card2) #On l'ajoute à la combinaison à tester
                if side[0] == (0,0): #Si la combinaison n'est toujours pas complète
                    for card3 in unrevealedCards: #Pour chaque cartes non-révélées
                        if card3 == card1 or card3 == card2: #Si elle est différente de la première et la deuxième carte ajoutée (on évite de créer des doublons)
                            continue
                        else:
                            side.append(card3) #On l'ajoute à la combinaison à tester

                        score = computePower_ai(side) #On calcule le score de la combinaison
                        score += computeSum_ai(side)/100 #On ajoute à ce nombre la somme des cartes divisée par 100 de sorte à ce qu'elle n'ai une importance que lorsque la combinaison est la même

                        if score > bestPotentialScore:
                            bestPotentialScore = score #On actualise le meilleur score

                        side.remove(card3) #On enlève la carte de la combinaison actuelle

                score = computePower_ai(side)
                score += computeSum_ai(side)/100

                if score > bestPotentialScore:
                    bestPotentialScore = score

                side.remove(card2) #On enlève la carte de la combinaison actuelle

        score = computePower_ai(side)
        score += computeSum_ai(side)/100

        if score > bestPotentialScore:
            bestPotentialScore = score

        side.remove(card1) #On enlève la carte de la combinaison actuelle

    return bestPotentialScore


def isDominating(player, frontier, unrevealedCards): #Fonction qui détermine si une frontière est dominée par un joueur même lorsque toutes les cartes ne sont pas posées

    side = [[],[]]

    for i in range(1,4):
        side[0].append(frontier[i])
    for i in range(4,7):
        side[1].append(frontier[i])

    if (player):
        opponent = 0
    else:
        opponent = 1

    return (bestPotentialScore(side[player],unrevealedCards) > bestPotentialScore(side[opponent],unrevealedCards)) #On retourne vrai si le meilleur score potentiel du joueur est supérieur à celui de son adversaire


def computeNumberDominatedFrontier(player, s): #Fonction qui calcule le nombre de frontières dominées par un joueur

    nb = 0

    for frontier in s[1]:
        if frontier[0] == -1 and (frontier[1] != (0,0) or frontier[4] != (0,0)): #On ne prend en compte une frontière que si elle est neutre et qu'une carte au moins est posée dessus
                if isDominating(player,frontier,unrevealedCards_ai(s[1])): #Si une frontière est dominée par le joueur, on incrémente de 1 notre compteur
                    nb += 1

    return nb

def eval4(player, s): #Quatrième fonction d'évaluation qui prend en compte le nombre de frontières dominées par un joueur

    if player:
        opponent = 0
    else:
        opponent = 1

    nbDominatedFrontier = computeNumberDominatedFrontier(player, s) #On calcule le nombre de frontières dominées par le joueur
    nbDominatedFrontierOpponent = computeNumberDominatedFrontier(opponent, s) #On calcule le nombre de frontières dominées par son adversaire

    nbMaxDominatedFrontier = 9 #Nombre maximum de frontières pouvant être dominées

    return (nbDominatedFrontier-nbDominatedFrontierOpponent)/nbMaxDominatedFrontier #Résultat entre -1 et 1

def isFinalState(player, s): #Fonction qui détermine si l'état en question est un état terminal (fonction homologue à isGameover)

    isFinalState = False
    
    nClaimedFrontier = 0
    nClaimedFrontierInARaw = 0

    for i in range(0, 9):
        if s[1][i][0] == player:
            nClaimedFrontier += 1
            nClaimedFrontierInARaw += 1
            if (nClaimedFrontierInARaw == 3 or nClaimedFrontier == 5):
                isFinalState = True
        else:
            nClaimedFrontierInARaw = 0

    return isFinalState

def eval(player, s): #Fonction d'évaluation d'un état

    if isFinalState(player, s): #Si l'état est terminal, on lui attribut le score maximale
        score = 1
    else:
        score = W1*eval1(player, s)+W2*eval2(player, s)+W3*eval3(player, s)+W4*eval4(player, s) #Décomposition de la fonction en plusieurs sous-fonctions d'évaluations

    return score

def alphaBeta(player, s, p): #Algorithme de type MinMax avec élagage AlphaBeta

    #On inclut dans la fonction une itération de la fonction maxValue afin de conserver une trace du coup à jouer en premier

    alpha = -1
    beta = 1

    val = -1
    for ns in nextState(player, s):
        minVal = minValue(player, ns[0], p-1, alpha, beta)
        if minVal > val:
            val = minVal
            bestplay = ns

        alpha = max(alpha,val)
        
    return bestplay

def maxValue(player, s, p, alpha, beta): #Fonction maxValue de l'algorithme MinMax avec élagage AlphaBeta qui renvoie une valeur de gain maximale

    if eval(player, s) == 1 or eval(player, s) == -1 or p == 0:
        return eval(player, s)
    else:
        val = -1
        for ns in nextState(player, s):
            val = max(val, minValue(player, ns[0], p-1, alpha, beta))
            if val >= beta:
                return val
            alpha = max(alpha,val)

        return val

def minValue(player, s, p, alpha, beta): #Fonction minValue de l'algorithme MinMax avec élagage AlphaBeta qui renvoie une valeur de gain minimale

    if eval(player, s) == 1 or eval(player, s) == -1 or p == 0:
        return eval(player, s[0])
    else:
        val = 1
        for ns in nextStateOpponent(player, s):
            val = min(val, maxValue(player, ns[0], p-1, alpha, beta))
            if val <= alpha:
                return val
            beta = min(beta,val)

        return val