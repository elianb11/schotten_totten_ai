from Card import *
import pygame
from Frontier import *
from Hand import *
import math

class Gameboard: #Classe représentant le plateau de jeu

    def __init__(self, expert):

        self.expert_mode = expert #Booléen indiquant si la partie se déroule en mode expert ou non
        self.frontiers_visual, self.frontiers_p0_rect, self.frontiers_p1_rect, self.frontiers_p2_rect = self.initializeFrontiers() #Visuels des frontières
        self.cards_visual = self.initializeCards() #Visuels des cartes
        self.frontiers = [] #Liste des objets "Frontier"
        for i in range(0, 9): #On initialise les objets "Frontier"
            self.frontiers.append(Frontier(i))
        self.ClanCardDraw = Card_Draw("Clan") #On initialise la pioche de cartes de clan
        if expert: #Si la partie se déroule en mode expert 
            self.TacticCardDraw = Card_Draw("Tactic") #On initialise la pioche de cartes tactiques
            self.nTacticCardPlayed = [0, 0] #Nombre de cartes tactiques jouées par les deux joueurs
            self.DiscardPile = [] #Liste de cartes défaussées
        self.hands = [Hand(expert), Hand(expert)] #On initialise les objets "Hand" des deux joueurs
        self.hands[0].fillHand(self.ClanCardDraw) #On remplit la main du premier joueur
        self.hands[1].fillHand(self.ClanCardDraw) #On remplit la main du second joueur
        self.player1_cards_rect, self.player2_cards_rect = self.initializeHandCardsRect() #Positions des cartes des mains des joueurs
        self.frontiers_sides_cards_rect = self.initializeSideCardsRect() #Positions des cartes jouées
        self.winner = 0
    

    def initializeCards(self): #Fonction qui crée les visuels des cartes de jeu

        WHITE = (255,255,255)
        BG_COLOR = (232, 217, 206)
        GREEN = (170,201,35)
        PURPLE = (192,84,169)
        RED = (243,47,33)
        BLUE = (91,201,228)
        YELLOW = (242,203,22)
        BROWN = (214,149,117)
        colors = [GREEN,PURPLE,RED,BLUE,YELLOW,BROWN]
        colors_name = ["green","purple","red","blue","yellow","brown"]

        font = pygame.font.Font("resources/Roboto-bold.ttf", 20)

        image = pygame.image.load("resources/icon.png")
        image = pygame.transform.scale(image, (45,45))
        image_rect = image.get_rect()
        image_rect.x = math.ceil(10)
        image_rect.y = math.ceil(28)

        cards = {}
        
        j=0
        for color in colors: #Pour chaque couleur de cartes
            for i in range(1,10): #Pour chaque numéro de cartes
                card = pygame.Surface((65,100)) #Création de la surface de la nouvelle carte
                card_rect = card.get_rect()
                card.fill(BG_COLOR)
                pygame.draw.rect(card, WHITE, card_rect, border_radius=5)
                card_number = font.render(str(i), True, color)
                card_number_rect = card_number.get_rect()
                card_number_rect.x = math.ceil(48)
                card_number_rect.y = math.ceil(2)
                card_number_rect2 = card_number.get_rect()
                card_number_rect2.x = math.ceil(4)
                card_number_rect2.y = math.ceil(75)
                card.blit(card_number,card_number_rect)
                card.blit(card_number,card_number_rect2)
                card.blit(image,image_rect)
                cards[i,colors_name[j]] = card #Ajout du visuel de la carte au dictionnaire des cartes
            j += 1
        
        return cards

    def initializeHandCardsRect(self): #Fonction qui crée les positions des cartes de jeu dans la main des joueurs

        player1_cards_rect = []
        player2_cards_rect = []

        i=0
        for hand in self.hands:
            x = 100
            y0 = 570
            y1 = 20
            for card in hand.Cards:
                card_visual = self.cards_visual[card.Value, card.Color]
                card_rect = card_visual.get_rect()
                if i == 0:
                    card_rect.x = math.ceil(x)
                    card_rect.y = math.ceil(y0)
                    player1_cards_rect.append(card_rect)
                elif i == 1:
                    card_rect.x = math.ceil(x)
                    card_rect.y = math.ceil(y1)
                    player2_cards_rect.append(card_rect)
                x += 90
            i += 1

        return player1_cards_rect, player2_cards_rect

    def initializeSideCardsRect(self): #Fonction qui crée les positions des cartes jouées autour des frontières

        frontiers_sides_cards_rect = []
        x=28
        for i in range(0,9):
            frontier_sides_cards_rect = []
            y=390
            side1 = []
            for j in range(0,3):
                card_rect = self.cards_visual[1,"red"].get_rect()
                card_rect.x = math.ceil(x)
                card_rect.y = math.ceil(y)
                side1.append(card_rect)
                y += 25
            frontier_sides_cards_rect.append(side1)
            y = 210
            side2 = []
            for j in range(0,3):
                card_rect = self.cards_visual[1,"red"].get_rect()
                card_rect.x = math.ceil(x)
                card_rect.y = math.ceil(y)
                side2.append(card_rect)
                y -= 25
            frontier_sides_cards_rect.append(side2)
            frontiers_sides_cards_rect.append(frontier_sides_cards_rect)
            x += 110

        return frontiers_sides_cards_rect


    def initializeFrontiers(self): #Fonction qui crée les visuels et les postions des frontières (positions en fonction de l'état de la frontière)
        frontier_image_1 = pygame.image.load("resources/frontier_1.png") #Importation des visuels depuis les ressources images
        frontier_image_1 = pygame.transform.scale(frontier_image_1, (100,100)) #Redimensionnement du visuel
        frontier_image_2 = pygame.image.load("resources/frontier_2.png")
        frontier_image_2 = pygame.transform.scale(frontier_image_2, (100,100))
        frontier_image_3 = pygame.image.load("resources/frontier_3.png")
        frontier_image_3 = pygame.transform.scale(frontier_image_3, (100,100))
        frontier_images = [frontier_image_1, frontier_image_2, frontier_image_3]

        frontiers = [] #visuels
        frontiers_p0_rect = [] #positions neutre
        frontiers_p1_rect = [] #positions joueur 1
        frontiers_p2_rect = [] #positions joueur 2

        j = 0
        x = 10
        y = 300
        for i in range(0,9):
            frontiers.append(frontier_images[j])
            frontiers_p0_rect.append(frontiers[i].get_rect())
            frontiers_p0_rect[i].x = math.ceil(x)
            frontiers_p0_rect[i].y = math.ceil(y)
            frontiers_p1_rect.append(frontiers[i].get_rect())
            frontiers_p1_rect[i].x = math.ceil(x)
            frontiers_p1_rect[i].y = math.ceil(y+160)
            frontiers_p2_rect.append(frontiers[i].get_rect())
            frontiers_p2_rect[i].x = math.ceil(x)
            frontiers_p2_rect[i].y = math.ceil(y-160)
            j += 1
            x += 110
            if j == 3:
                j = 0

        return frontiers, frontiers_p0_rect, frontiers_p1_rect, frontiers_p2_rect


    def displayFrontiers(self, screen): #Fonction d'affichage des frontières
            
        i=0
        for frontier in self.frontiers: #Vérifie le status de chaque frontière et affiche en conséquence sur la surface principale
            if frontier.Status == -1:
                screen.blit(self.frontiers_visual[i], self.frontiers_p0_rect[i])
            elif frontier.Status == 0:
                screen.blit(self.frontiers_visual[i], self.frontiers_p1_rect[i])
            elif frontier.Status == 1:
                screen.blit(self.frontiers_visual[i], self.frontiers_p2_rect[i])
            i += 1

        return screen

    def displayHands(self, screen, turn): #Fonction d'affichage des mains des joueurs
        
        i=0
        for hand in self.hands: #Pour chacune des deux mains des joueurs
            x = 100
            y0 = 570
            y1 = 20
            for card in hand.Cards: #Pour chaque carte de la main
                card_visual = self.cards_visual[card.Value, card.Color] #Récupère le visuel de la carte
                back_card = pygame.image.load("resources/back_card.png") #Visuel de dos de carte
                back_card = pygame.transform.scale(back_card, (65,100))
                arrow = pygame.image.load("resources/arrow.png") #Flêche d'indication visuelle
                arrow_rect = arrow.get_rect()
                arrow_rect.x = math.ceil(25)
                arrow = pygame.transform.scale(arrow, (65,65))
                card_rect = card_visual.get_rect()
                if i == 0: #Main du joueur 1
                    card_rect.x = math.ceil(x)
                    card_rect.y = math.ceil(y0)
                    if turn % 2: #Si c'est au tour du joueur 1, affichage des cartes du joueur 1 retournées
                        arrow_rect.y = math.ceil(y0+15)
                        screen.blit(arrow, arrow_rect)
                        screen.blit(card_visual, card_rect)
                    else:
                        screen.blit(back_card, card_rect) #affichage des cartes du joueur 1 non retournées
                elif i == 1: #Main du joueur 2
                    card_rect.x = math.ceil(x)
                    card_rect.y = math.ceil(y1)
                    if not turn % 2: #Si c'est au tour du joueur 2, affichage des cartes du joueur 2 retournées
                        arrow_rect.y = math.ceil(y1+15)
                        screen.blit(arrow, arrow_rect)
                        screen.blit(card_visual, card_rect)
                    else:
                        screen.blit(back_card, card_rect) #affichage des cartes du joueur 2 non retournées
                x += 90
            i += 1

        return screen

    def displaySides(self, screen): #Fonction d'affichage des cartes jouées autour des frontières
        
        j=0
        for frontier in self.frontiers: #Pour chaque frontière
            frontier_cards_rect = self.frontiers_sides_cards_rect[j]
            i=0
            for side in frontier.Side: #Pour chacun des deux côtés de la frontière
                k=0
                for card in side.Cards: #Pour chaque carte de ce coté de la  frontière
                    card_visual = self.cards_visual[card.Value, card.Color] #Récupération du visuel de la carte
                    card_rect = frontier_cards_rect[i][k]
                    screen.blit(card_visual, card_rect) #Affichage de la carte sur la surface principale de jeu
                    k+=1
                i+=1
            j+=1
        return screen


    def isGameover(self): #Méthode qui vérifie si la partie est terminée ou non

        gameover = False 

        for player in range(0, 2): #Pour chaque joueurs...
            nClaimedFrontier = 0 #Nombre de frontières revendiquées
            nClaimedFrontierInARaw = 0 #Nombre de frontières revendiquées à la suite
            for i in range(0, 9): #Pour chaque frontières...
                if (self.frontiers[i].Status == player): #La statut d'appartenance de la frontière correspond à l'indice du joueur
                    nClaimedFrontier += 1 #On incrémente de 1 le nombre de frontières revendiquées
                    nClaimedFrontierInARaw += 1 #On incrémente de 1 le nombre de frontières revendiquées à la suite
                    if (nClaimedFrontierInARaw == 3 or nClaimedFrontier == 5): #Si le nombre de frontières revendiquées est de 5 ou le nombre de frontières revendiquées à la suite est de 3...
                        gameover = True #La partie est fini
                        winner = player
                else:
                    nClaimedFrontierInARaw = 0 #Sinon on remet le compteur de frontières revendiquées à la suite à 0

        if (gameover):
            self.winner = winner
            print("Le joueur {} est le gagnant !".format(winner))

        return gameover

    def unrevealedCards(self): #Méthode qui renvoie une liste de toutes les cartes qui n'ont pas été révélées de la partie

        unrevealedCards = [] #On créé cette liste

        for card in self.hands[0].Cards:
            unrevealedCards.append(card) #On inclut dans cette liste toutes les cartes de la main du premier joueur
        for card in self.hands[1].Cards:
            unrevealedCards.append(card) #On inclut dans cette liste toutes les cartes de la main du second joueur
        for card in self.ClanCardDraw.Cards:
            unrevealedCards.append(card) #On inclut également dans cette liste toutes les cartes de la pioche de carte clan
        if (self.expert_mode):
            for card in self.TacticCardDraw.Cards:
                unrevealedCards.append(card) #Si le mode est expert, on rajoute les cartes de la pioche tactique

        return unrevealedCards

    """
    def unknownCards(self, player):

        unknownCards = []

        if player:
            opponent = 0
        else:
            opponent = 1

        for card in self.hands[opponent].Cards:
            unrevealedCards.append(card)
        for card in self.ClanCardDraw.Cards:
            unrevealedCards.append(card)
        if (self.expert_mode):
            for card in self.TacticCardDraw.Cards:
                unrevealedCards.append(card)

        return unknownCards
    """

    def generateState(self, player): #Méthode renvoyant l'état actuel du jeu

        state = [] #Liste représentant l'état

        state.append(self.hands[player].generateState()) #On ajoute à cette liste la forme simplifiée de la main

        state_frontiers = [] #Liste des formes simplifiées des frontières

        for frontier in self.frontiers: #Pour chaque frontières...

            state_frontiers.append(frontier.generateState()) #On rajoute à la liste la forme simplifiée de la frontière en question

        state.append(state_frontiers) #On les formes simplifiées de nos frontières à la liste état

        return state

    def __str__(self): #Méthode affichant l'objet (phases de test)

        concat = "\n-----------------------------------------------------------------------------------------------------------------------------------\nPLAYER 2\n\n"
        concat += self.hands[1].__str__()
        concat += "\n\n"
        concat += "     Side 1                                                                                                              Side 2\n"
        for i in range(9):
            concat += self.frontiers[i].__str__()
        concat += "\n\n"
        concat += self.hands[0].__str__()
        concat += "\nPLAYER 1\n-----------------------------------------------------------------------------------------------------------------------------------\n"

        return concat