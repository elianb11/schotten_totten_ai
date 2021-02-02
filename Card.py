import random

COLORS = {1: "red", 2: "green", 3: "blue",4: "yellow", 5: "purple", 6: "brown"} #Dictionnaire des couleurs et leurs entiers correspondants
ELITE_TROOP_CARDS = {1: "JOKER", 2: "SPY", 3: "SHIELD HOLDER"} #Dictionnaire des cartes troupes d'élite et leurs entiers correspondants
FIGHT_MODE_CARDS = {1: "COMBAT DE BOUE", 2: "COLLIN-MAILLARD"} #Dictionnaire des cartes combats et leurs entiers correspondants"
RUSE_CARDS = {1: "HEAD HUNTER", 2: "STRATEGIST", 3: "BANSHEE", 4: "TRAITOR"} #Dictionnaire des cartes ruses et leurs entiers correspondants#

SUITE_COLOR = 4 #On affecte à chaque combinaison une puissance sous forme d'un entier
BRELAN = 3
COLOR = 2
SUITE = 1

def find_key(dic,v): #Fonction qui retourne la clé associée à une valeur donnée dans un dictionnaire 

    for k, val in dic.items(): 
        if v == val: 
            return k

class Card: #Classe abstraite représentant une carte

    def __init__(self, type):
        self.Type = type


class Clan(Card): #Classe représentant une carte de clan

    def __init__(self, value, color):

        self.Type = "Clan"
        self.Value = value
        self.Color = color

    def __str__(self): #Méthode affichant l'objet (phases de test)

        return "|{} CLAN {}|".format(self.Value, self.Color)

    def __eq__(self, card):

        return (self.Value == card.Value and self.Color == card.Color)


class Elite_Troop(Clan): #Classe représentant une carte troupe d'élite

    def __init__(self, name):

        self.Type = "Tactic"
        self.Name = name
        if name == "JOKER":
            self.Value = 0
            self.Color = "?"
        if name == "SPY":
            self.Value = 7
            self.Color = "?"
        if name == "SHIELD HOLDER":
            self.Value = 0
            self.Color = "?"

    def __str__(self): #Méthode affichant l'objet (phases de test)

        return "|{} {} {}|".format(self.Value, self.Name, self.Color)

    def chooseAttributes(self):

        if self.Name == "JOKER":
            while self.Value < 1 or self.Value > 9:
                self.Value = int(
                    input("Choisissez la valeur de votre carte Shield Holder -> "))
            while self.Color != "red" and self.Color != "green" and self.Color != "blue" and self.Color != "yellow" and self.Color != "purple" and self.Color != "brown":
                self.Color = input(
                    "Choisissez la couleur de votre carte Shield Holder -> ")
        if self.Name == "SPY":
            while self.Color != "red" and self.Color != "green" and self.Color != "blue" and self.Color != "yellow" and self.Color != "purple" and self.Color != "brown":
                self.Color = input(
                    "Choisissez la couleur de votre carte Shield Holder -> ")
        if self.Name == "SHIELD HOLDER":
            while self.Value < 1 or self.Value > 3:
                self.Value = int(
                    input("Choisissez la valeur de votre carte Shield Holder -> "))
            while self.Color != "red" and self.Color != "green" and self.Color != "blue" and self.Color != "yellow" and self.Color != "purple" and self.Color != "brown":
                self.Color = input(
                    "Choisissez la couleur de votre carte Shield Holder -> ")


class Fight_Mode(Card): #Classe représentant une carte combat

    def __init__(self, name, effect):

        self.Type = "Tactic"
        self.Name = name
        self.Effect = effect

    def __str__(self): #Méthode affichant l'objet (phases de test)

        return "|X| {} |X|".format(self.Name)


class Ruse(Card): #Classe représentant une carte ruse

    def __init__(self, name, effect):

        self.Type = "Tactic"
        self.Name = name
        self.Effect = effect

    def __str__(self): #Méthode affichant l'objet (phases de test)
 
        return "|O| {} |O|".format(self.Name)


class Card_Draw: #Classe représentant la pioche

    def __init__(self, type):

        self.Type = type #Type clan ou tactic (mode expert uniquement)
        self.Cards = [] #Liste de cartes qui composent la pioche
        if type == "Clan": #Si c'est une pioche de type clan, la remplir de carte clan sinon la remplir de cartes tactiques
            self.fillClanDraw()
            self.Size = 54
        else:
            self.fillTacticDraw()
            self.Size = 10
        self.shuffleCards() #On mélange le paquet de cartes

    def fillClanDraw(self): #Méthode ajoutant toutes les cartes clan initialement contenues dans la pioche

        for color in COLORS.values():
            for i in range(1, 10):
                self.Cards.append(Clan(i, color))

    def fillTacticDraw(self): #Méthode ajoutant toutes les cartes tactic initialement contenues dans la pioche

        self.Cards.append(Elite_Troop("JOKER"))
        for card in ELITE_TROOP_CARDS.values():
            self.Cards.append(Elite_Troop(card))
        for effect, card in FIGHT_MODE_CARDS.items():
            self.Cards.append(Fight_Mode(card, effect))
        for effect, card in RUSE_CARDS.items():
            self.Cards.append(Ruse(card, effect))

    def shuffleCards(self): #Méthode mélangant la liste des cartes

        random.shuffle(self.Cards)

    def draw(self): #Méthode retournant la carte en tête de liste (supprimant également la carte de la liste) simulant la pioche

        card = self.Cards.pop(0)
        self.Size -= 1

        return card

    def isEmpty(self): #Méthode retournant si la liste de cartes en vide ou non

        return (self.Size == 0)

    def __str__(self): #Méthode affichant l'objet (phases de test)

        concat = ""
        if self.Type == "Clan":
            n = 0
            for card in self.Cards:
                concat += card.__str__()
                concat += " "
                n += 1
                if n % 9 == 0:
                    concat += "\n"
        else:
            for card in self.Cards:
                concat += card.__str__()
                concat += " "
            concat += "\n"

        return concat

def computePower(Cards): #Fonction retournant la puissance associée à une combinaison de cartes donnée

    power = 0 #On initialise la puissance à 0 dans le cas où il n'y aurait pas de combinaison particulière

    if (isSuite(Cards) and isColor(Cards)):
        power = SUITE_COLOR
    else:
        if (isBrelan(Cards)):
            power = BRELAN
        if (isColor(Cards)):
            power = COLOR
        if (isSuite(Cards)):
            power = SUITE

    return power


def computeSum(Cards): #Fonction retournant la somme des cartes d'une combinaison donnée

    sum = 0
    for card in Cards:
        sum += card.Value

    return sum


def isColor(Cards): #Fonction déterminant si la combinaison de carte est une couleur

    isColor = True
    color = Cards[0].Color #On vérifie la couleur du premier élément de la liste de carte

    for card in Cards:
        if card.Color != color: #Si un élément est de couleur différente, ce n'est pas une couleur
            isColor = False
            break

    return isColor


def isBrelan(Cards): #Fonction déterminant si la combinaison de carte est un brelan

    isBrelan = True
    value = Cards[0].Value #On vérifie la valeur du premier élément de la liste de carte

    for card in Cards:
        if card.Value != value: #Si un élément a une valeur différente, ce n'est pas un brelan
            isBrelan = False
            break

    return isBrelan


def isSuite(Cards): #Fonction déterminant si la combinaison de carte est une suite

    suite = True

    list_values = []
    for card in Cards:
        list_values.append(card.Value) #On créé la liste des valeurs des cartes

    list_values.sort() #On la trie"

    firstValue = list_values.pop(0) #On vérifie la première valeur
    n = 1
    for i in list_values:        
        if i != firstValue + n: #Si les valeurs suivantes ne sont pas issues de l'incrémentation successive de la première, ce n'est pas une suite
            suite = False
        n+=1

    return suite