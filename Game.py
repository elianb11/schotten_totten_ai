import Card
from Gameboard import *
from Ai import *
from Player import *
import random
import pygame
pygame.init()

class Game(): #Classe représentant une partie de Schotten Totten

    def __init__(self, ai_opponent, expert, player1_name, player2_name):

        self.is_ai_opponent = ai_opponent #Booléen indiquant si une ia est présente ou non
        self.gameboard = Gameboard(expert) #On initialise le plateau de jeu
        self.player1 = Player(player1_name, 0, self.gameboard, self.gameboard.hands[0]) #On initialise le joueur 1
        self.player2 = Player(player2_name, 1, self.gameboard, self.gameboard.hands[1]) #On initialise le joueur 2
        self.Turn = 1 #Numéro du tour
        self.turnIsDone = True #Booléen indiquant si le tour est terminé ou non
        self.message = "" #Message à afficher sur la fenêtre de jeu
        self.scene = pygame.Surface #Surface d'affichage principale de la fenêtre de jeu
        self.selectedCardNumber = -1 #Numéro de carte sélectionnée (-1: pas de carte sélectionnée)
        self.selectedFrontierNumber = -1 #Numéro de frontière sélectionnée (-1: pas de carte sélectionnée)
        self.frontierClaimNumber = -1 #Numéro de frontière à revendiquer sélectionnée (-1: pas de carte sélectionnée)
        self.cards_stack = pygame.image.load("resources/cards_stack.png") #Visuel de la pile de cartes
        self.cards_stack_rect = self.cards_stack.get_rect()
        self.skip_button = pygame.image.load("resources/button_skip_turn.png") #Bouton SKIP TURN
        self.skip_button_rect = self.skip_button.get_rect()


    def displayGame(self): #Fonction d'affichage de la fenêtre de jeu

        GAME_WIN_H = 800 #Taille de la fenêtre de jeu
        GAME_WIN_W = 1120
        BG_COLOR = (232, 217, 206) #Couleur de l'arrière plan

        if self.gameboard.expert_mode: #Changement du titre de la fenêtre suivant le mode de jeu
            if self.is_ai_opponent:
                print("Game VS AI is launched in expert mode")
                pygame.display.set_caption("Schotten Totten - Game VS AI - Expert mode")
            else:
                print("Game 1V1 is launched in expert mode")
                pygame.display.set_caption("Schotten Totten - Game 1V1 - Expert mode")
        else:
            if self.is_ai_opponent:
                print("Game VS AI is launched in normal mode")
                pygame.display.set_caption("Schotten Totten - Game VS AI - Normal mode")
            else:
                print("Game 1V1 is launched in normal mode")
                pygame.display.set_caption("Schotten Totten - Game 1V1 - Normal mode")

        print("Player 1 name is " + self.player1.name)
        print("Player 2 name is " + self.player2.name)

        self.scene = pygame.display.set_mode((GAME_WIN_W, GAME_WIN_H))
        
        self.cards_stack = pygame.transform.scale(self.cards_stack,(79,109)) #Placement du visuel de la pile de cartes sur la fenêtre
        self.cards_stack_rect.x = math.ceil(1020)
        self.cards_stack_rect.y = math.ceil(300)

        self.skip_button = pygame.transform.scale(self.skip_button, (214,60)) #Placement du bouton SKIP sur la fenêtre
        self.skip_button_rect.x = math.ceil(890)
        self.skip_button_rect.y = math.ceil(625)

        game_running = True

        while game_running:

            for event in pygame.event.get(): #Gestionnaires des évènements de jeu
                if event.type == pygame.QUIT: #Evènement de fermeture du jeu
                    game_running = False
                    pygame.quit()
                    print("Game is closed")
                if event.type == pygame.MOUSEBUTTONDOWN: #Evènement de type clic souris
                    for i in range(0,6):
                        if self.gameboard.player1_cards_rect[i].collidepoint(event.pos) and self.Turn % 2:
                            print("card "+ str(i+1) +" has been selected by player1")
                            self.selectedCardNumber = i
                    for i in range(0,6):
                        if self.gameboard.player2_cards_rect[i].collidepoint(event.pos) and not self.Turn % 2:
                            print("card "+ str(i+1) +" has been selected by player2")
                            self.selectedCardNumber = i
                    for i in range(0,9):
                        if self.gameboard.frontiers_p0_rect[i].collidepoint(event.pos):
                            print("frontier "+ str(i+1) +" has been selected")
                            self.selectedFrontierNumber = i

            if self.gameboard.isGameover(): #Si la partie est gagnée par un joueur
                self.scene.fill(BG_COLOR)
                if self.gameboard.winner == 0:
                    self.message = "{} is the WINNER, congratulations!".format(self.player1.name)
                elif self.gameboard.winner == 1:
                    self.message = "{} is the WINNER, congratulations!".format(self.player2.name)
                self.displayMessage()
                pygame.display.flip()
            else:
                self.updateScene() #Mise à jour de la fenêtre de jeu
                self.playTurn() #Permet au tour de se jouer le tour si les conditions sont remplies (voir fonction)

    
    def updateScene(self): #Fonction qui crée une nouvelle surface du jeu en la mettant à jour

        BG_COLOR = (232, 217, 206)

        self.scene.fill(BG_COLOR)
        if self.message != "":
            self.displayMessage()
        self.scene.blit(self.cards_stack, self.cards_stack_rect)
        self.scene.blit(self.skip_button, self.skip_button_rect)
        self.scene = self.gameboard.displaySides(self.scene)
        self.scene = self.gameboard.displayFrontiers(self.scene)
        self.scene = self.gameboard.displayHands(self.scene, self.Turn)
        pygame.display.flip()



    def displayMessage(self): #Fonction d'affichage du message en attribut de la classe

        WHITE = (255,255,255)
        BG_COLOR = (232, 217, 206)
        BROWN = (155,111,76)

        font = pygame.font.Font("resources/Roboto-bold.ttf", 25)

        block = pygame.Surface((1110,100)) #Création de la surface blanche de fond du message
        block_rect = block.get_rect()
        block.fill(BG_COLOR)
        pygame.draw.rect(block, WHITE, block_rect, border_radius=5)
        block_rect.x = math.ceil(5)
        block_rect.y = math.ceil(695)

        if len(self.message) > 100: #Affichage du message sur deux lignes si il est trop long
            line1 = self.message[0:90] + '-'
            line2 = self.message[90:]

            message2 = font.render(line2, True, BROWN) #Création du visuel du texte du message sur la ligne 2
            message2_rect = message2.get_rect()
            message2_rect.x = math.ceil(10)
            message2_rect.y = math.ceil(50)

            block.blit(message2, message2_rect)
        else:
            line1 = self.message

        message1 = font.render(line1, True, BROWN) #Création du visuel du texte du message
        message1_rect = message1.get_rect()
        message1_rect.x = math.ceil(10)
        message1_rect.y = math.ceil(10)

        block.blit(message1,message1_rect) #Affichage du texte du message sur la surface blanche
        self.scene.blit(block, block_rect) #Affichage du bloc message sur la fenêtre de jeu


    def playTurn(self): #Fonction qui gère les tours des joueurs et qui appelle la fonction play()

        if self.is_ai_opponent and not (self.Turn % 2): #Si c'est au tour de l'IA de jouer (joueur 2)
            self.turnIsDone = False
            self.playAI(self.player2)
            self.Turn += 1
            self.selectedCardNumber = -1
            self.selectedFrontierNumber = -1
            self.turnIsDone = True
        elif self.selectedCardNumber != -1 and self.selectedFrontierNumber != -1 and self.turnIsDone: #Si une carte et une frontière sont sélectionnées
            self.turnIsDone = False
            if (self.Turn % 2): #Tour du joueur 1
                self.message = "Player 1 turn: {}. Select a card and a frontier.".format(self.player1.name)
                self.displayMessage()
                self.play(self.player1)
            else: #Tour du joueur 2 (Si le mode IA n'est pas sélectionné)
                self.message = "Player 2 turn: {}. Select a card and a frontier.".format(self.player2.name)
                self.displayMessage()
                self.play(self.player2)
            self.Turn += 1
            self.selectedCardNumber = -1
            self.selectedFrontierNumber = -1
            self.turnIsDone = True
        else:
            if (self.Turn % 2):
                self.message = "Player 1 turn: {}. Select a card and a frontier.".format(self.player1.name)
            else:
                self.message = "Player 2 turn: {}. Select a card and a frontier.".format(self.player2.name)  

    def play(self, player): #Fonction qui permet au joueur passé en paramètre de jouer son tour

        if (player.Hand.Cards[(self.selectedCardNumber)].Type == "Clan"):
            player.playTroop(self.selectedCardNumber, self.selectedFrontierNumber)
        self.scene = self.gameboard.displaySides(self.scene)

        self.message = "Do you want to claim a frontier ? If yes, select a frontier, else, you can skip the turn."

        self.updateScene()

        while(self.turnIsDone == False):
            for event in pygame.event.get(): #Gestionnaire d'évènement
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("Game is closed")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0,9):
                        if self.gameboard.frontiers_p0_rect[i].collidepoint(event.pos): #Si clic sur une frontière à revendiquer
                            print("frontier "+ str(i+1) +" has been selected")
                            self.frontierClaimNumber = i
                    if self.skip_button_rect.collidepoint(event.pos): #Si clic sur le bouton SKIP
                        self.turnIsDone = True
            if self.frontierClaimNumber != -1:
                self.message = player.claimFrontier(self.frontierClaimNumber) #Tentative de revendication de la frontière sélectionnée
                self.updateScene()
                self.frontierClaimNumber = -1

        player.draw()

    def playAI(self, player): #Fonction qui permet à l'IA (joueur 2 passé en paramètre) de jouer son tour

        play = alphaBeta(player.number, self.gameboard.generateState(player.number), 2)
        print(play)
        self.selectedCardNumber = play[1]
        self.selectedFrontierNumber = play[2]

        if (player.Hand.Cards[(self.selectedCardNumber)].Type == "Clan"):
            player.playTroop(self.selectedCardNumber, self.selectedFrontierNumber)

        if len(play[3]) != 0: #Revendication des frontières
            for frontierClaimNumber in play[3]:
                self.frontierClaimNumber = frontierClaimNumber
                player.claimFrontier(self.frontierClaimNumber)
                self.updateScene()
            self.frontierClaimNumber = -1

        player.draw()
        self.turnIsDone = True

        


