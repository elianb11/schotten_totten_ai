from MainMenu import *
from Game import *

mainMenu = MainMenu() #Création de l'objet lié à l'affichage du menu principal

mainMenu.displayMainMenu() #Affichage du menu principal

game = Game(mainMenu.ai_opponent, mainMenu.expert_mode, mainMenu.player1_name, mainMenu.player2_name) #Création de l'objet lié au lancement de la partie. On passe en arguement les modes sélectionnés et le nom des joueurs 

game.displayGame() #Affichage de la partie