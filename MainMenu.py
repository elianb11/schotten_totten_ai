import pygame
import math
import Card
import copy
pygame.init()

class MainMenu(): #Classe contenant l'interface graphique de lancement du jeu

    def __init__(self):
        self.expert_mode = False
        self.ai_opponent = False
        self.player1_name = ''
        self.player2_name = ''
        
    def displayMainMenu(self): #Fonction permettant d'afficher et de gérer les évenements de la fenêtre d'accueil

        MAIN_WIN_H = 751 #Taille de la fenêtre
        MAIN_WIN_W = 600

        pygame.display.set_caption("Schotten Totten") #Titre de la fenêtre
        screen = pygame.display.set_mode((MAIN_WIN_W, MAIN_WIN_H)) #Création de la surface principale

        background = pygame.image.load("resources/schotten_totten_main_menu.png")
        
        icon = pygame.image.load("resources/icon.png")
        pygame.display.set_icon(icon)

        start_1v1_button = pygame.image.load("resources/button_start_1v1.png") #Création du bouton "START 1V1"
        start_1v1_button_rect = start_1v1_button.get_rect()
        start_1v1_button_rect.x = math.ceil(171)
        start_1v1_button_rect.y = math.ceil(450)

        start_vs_ai_button = pygame.image.load("resources/button_start_vs_ai.png") #Création du bouton "START VS AI"
        start_vs_ai_button_rect = start_vs_ai_button.get_rect()
        start_vs_ai_button_rect.x = math.ceil(171)
        start_vs_ai_button_rect.y = math.ceil(540)

        expert_mode_label = pygame.image.load("resources/label_expert_mode.png") #Création du label "EXPERT MODE"

        off_button = pygame.image.load("resources/button_off.png") #Création du bouton "ON" et "OFF"
        on_button = pygame.image.load("resources/button_on.png")
        off_on_button_rect = off_button.get_rect()
        off_on_button_rect.x = math.ceil(401)
        off_on_button_rect.y = math.ceil(630)
        off_on_button_state = False

        screen.blit(background, (0,0)) #Affichage dees éléments crées sur la surface principale
        screen.blit(start_1v1_button, (171,450))
        screen.blit(start_vs_ai_button, (171,540))
        screen.blit(expert_mode_label, (101,635))
        screen.blit(off_button, (401,630))

        menu_running = True

        while menu_running:
            pygame.display.flip() #Rafraichissement de la surface d'affichage principale

            for event in pygame.event.get(): #Gestionnaire des évènements du menu
                if event.type == pygame.QUIT: #Evènement de fermeture du programme
                    menu_running = False
                    pygame.quit()
                    print("Game is closed")
                elif event.type == pygame.MOUSEBUTTONDOWN: #Evènements de type clics souris
                    if start_1v1_button_rect.collidepoint(event.pos): #Clic sur la surface du bouton "START 1V1"
                        print("START 1V1")
                        self.displayNameSelect() #Ouverture de la fenêtre de sélection des noms de joueurs
                        menu_running = False
                    elif start_vs_ai_button_rect.collidepoint(event.pos): #Clic sur la surface du bouton "START VS AI"
                        print("START VS AI")
                        self.displayNameSelect() #Ouverture de la fenêtre de sélection des noms de joueurs
                        menu_running = False
                        self.ai_opponent = True
                    elif off_on_button_rect.collidepoint(event.pos): #Clic sur la surface du bouton "ON" ou "OFF"
                        if(off_on_button_state):
                            print("EXPERT MODE ON TO OFF")
                            screen.blit(off_button, (401,630)) #Changement de l'état du bouton vers "OFF"
                            off_on_button_state = False
                            self.expert_mode = False
                        else:
                            print("EXPERT MODE OFF TO ON")
                            screen.blit(on_button, (401,630)) #Changement de l'état du bouton vers "ON"
                            off_on_button_state = True
                            self.expert_mode = True

    def displayNameSelect(self): #Fonction permettant d'afficher et de gérer les évenements de la fenêtre de sélection des noms de joueurs

        NAMESELECT_WIN_W = 650 #Taille de la fenêtre
        NAMESELECT_WIN_H = 350

        screen = pygame.display.set_mode((NAMESELECT_WIN_W, NAMESELECT_WIN_H))

        BROWN = (155, 111, 76)
        BLUE = (0, 175, 234)
        BG_COLOR = (232, 217, 206) #Couleur de l'arrière plan

        font = pygame.font.Font("resources/Roboto-bold.ttf", 40) #Police d'écriture du texte
        
        prompt1 = font.render('PLAYER 1 NAME : ', True, BROWN) #Création d'un label 'PLAYER 1 NAME : '
        prompt1_rect = prompt1.get_rect()
        prompt1_rect.x = math.ceil(30)
        prompt1_rect.y = math.ceil(50)

        prompt2 = font.render('PLAYER 2 NAME : ', True, BROWN) #Création d'un label 'PLAYER 2 NAME : '
        prompt2_rect = prompt2.get_rect()
        prompt2_rect.x = math.ceil(30)
        prompt2_rect.y = math.ceil(150)

        user_input1_value = "Benjamin" #Création du premier input qui correspond au premier nom
        user_input1 = font.render(user_input1_value, True, BROWN)
        user_input1_rect = user_input1.get_rect(topleft=prompt1_rect.topright)
        user_input1_state = False

        user_input2_value = "Elian" #Création du deuxième input qui correspond au deuxième nom
        user_input2 = font.render(user_input2_value, True, BROWN)
        user_input2_rect = user_input2.get_rect(topleft=prompt2_rect.topright)
        user_input2_state = False

        start_button = pygame.image.load("resources/button_start.png") #Création du bouton START
        start_button_rect = start_button.get_rect()
        start_button_rect.x = math.ceil(225)
        start_button_rect.y = math.ceil(240)

        done = False

        clock = pygame.time.Clock()

        while not done:

            for event in pygame.event.get(): #Gestionnaire des évènements
                if event.type == pygame.QUIT: #Evènement de fermeture du programme
                    done = True
                    pygame.quit()
                    print("Game is closed")   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_input1_rect.collidepoint(event.pos): #Si clic sur l'espace de l'input 1, changement de couleur de l'état de l'input
                        user_input1 = font.render(user_input1_value, True, BLUE)
                        user_input1_state = True
                        user_input2 = font.render(user_input2_value, True, BROWN)
                        user_input2_state = False
                    elif user_input2_rect.collidepoint(event.pos): #Si clic sur l'espace de l'input 2, changement de couleur de l'état de l'input
                        user_input2 = font.render(user_input2_value, True, BLUE)
                        user_input2_state = True
                        user_input1 = font.render(user_input1_value, True, BROWN)
                        user_input1_state = False
                    elif start_button_rect.collidepoint(event.pos): #Si clic sur le bouton START
                        done = True
                        print("Player names are choosed")
                        break
                    else:
                        user_input1 = font.render(user_input1_value, True, BROWN)
                        user_input1_state = False
                        user_input2 = font.render(user_input2_value, True, BROWN)
                        user_input2_state = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            done = True
                            print("Player names are choosed")
                            break
                    elif not user_input1_state and not user_input2_state: #Si aucun input n'est sélectionné
                        if event.key == pygame.K_TAB:
                            user_input1 = font.render(user_input1_value, True, BLUE)
                            user_input1_state = True
                    elif user_input1_state: #Si l'input 2 est sélectionné, gestion de l'entrée clavier sur l'input 1
                        if event.key == pygame.K_BACKSPACE:
                            user_input1_value = user_input1_value[:-1]
                            user_input1 = font.render(user_input1_value, True, BLUE)
                        elif event.key == pygame.K_TAB:
                            user_input2 = font.render(user_input2_value, True, BLUE)
                            user_input2_state = True
                            user_input1 = font.render(user_input1_value, True, BROWN)
                            user_input1_state = False
                        else:
                            user_input1_value += event.unicode #changement du texte de l'input 1
                            user_input1 = font.render(user_input1_value, True, BLUE)
                        user_input1_rect = user_input1.get_rect(topleft=prompt1_rect.topright)  
                    elif user_input2_state: #Si l'input 2 est sélectionné, gestion de l'entrée clavier sur l'input 2
                        if event.key == pygame.K_BACKSPACE:
                            user_input2_value = user_input2_value[:-1]
                            user_input2 = font.render(user_input2_value, True, BLUE)
                        elif event.key == pygame.K_TAB:
                            user_input1 = font.render(user_input1_value, True, BLUE)
                            user_input1_state = True
                            user_input2 = font.render(user_input2_value, True, BROWN)
                            user_input2_state = False
                        else:
                            user_input2_value += event.unicode #changement du texte de l'input 2
                            user_input2 = font.render(user_input2_value, True, BLUE)
                        user_input2_rect = user_input2.get_rect(topleft=prompt2_rect.topright)
                        

            clock.tick(30)
            screen.fill(BG_COLOR) #Création de la nouvelle surface à afficher
            screen.blit(prompt1, prompt1_rect)
            screen.blit(prompt2, prompt2_rect)
            screen.blit(user_input1, user_input1_rect)
            screen.blit(user_input2, user_input2_rect)
            screen.blit(start_button, start_button_rect)
            pygame.display.flip() #Rafraichissement de la fenêtre

        self.player1_name = user_input1_value #Changement des valeurs de noms des joueurs
        self.player2_name = user_input2_value
    


    


        

            
