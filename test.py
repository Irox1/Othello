#import pyxel
from math import inf
import re
import copy

class Game:
    def __init__(self) -> None:
        # Dictionnaire pour associer des couleurs à leurs codes
        #self.couleur = {0: "Vide", 1: "Blanc", 2: "Noir"}
        
        # Dictionnaire pour convertir les lettres (colonnes) en indices numériques
        self.coup = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        self.game_over__ = False
        
        # Dictionnaire inverse pour convertir les indices en lettres (colonnes)
        self.coup_inverse = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        
        # Regex pour valider les coups au format Othello (lettre a-h suivie d'un chiffre 1-8)
        self.regex_coup_othello = r"^[a-h][1-8]$"
        
        # Définition du joueur qui commence (Noir)
        self.turn = "Black"
        
        # Variable pour maintenir l'état du jeu (en cours ou non)
        self.running = True
        # Grille initiale du jeu avec pions blancs et noirs au centre
        self.actual_game = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def afficher_le_jeu(self, position):
        # Affiche la grille de jeu actuelle en console
        en_joli = {0: "🔸", 1: "⚪", 2: "⚫"}
        print("  1  2  3  4  5  6  7  8  ")
        ligne = ""
        for i in range(len(position)):
            ligne += self.coup_inverse[i]
            for j in position[i]:
                ligne += en_joli[j] + " "
            print(ligne)
            ligne = ""

    def game_over(self) ->bool:
        return len(self.coup_disponible()) == 0

    def minimax(self, depth : int, maximizingPlayer: bool, position): #Blanc = True et Noir = False
        #L'algorithme MiniMax
        if depth == 0 or self.game_over__:
            resultat = self.compter_pions(position)
            return resultat[0] - resultat[1]
        
        if maximizingPlayer:
            maxEval = -inf
            for coup in self.coup_disponible():
                copy_du_tableau = copy.deepcopy(position)
                self.simulation(copy_du_tableau,coup)
                evaluation = self.minimax(depth-1, False, copy_du_tableau)
                maxEval = max(maxEval, evaluation)
            return maxEval
        else:
            minEval = +inf
            for coup in self.coup_disponible():
                copy_du_tableau = copy.deepcopy(position)
                self.simulation(copy_du_tableau,coup)
                evaluation = self.minimax(depth-1, True, copy_du_tableau)
                minEval = min(minEval, evaluation)
            return minEval

    def simulation(self, position, coup):
        self.play_move(coup, position)
                
    def ia_joue(self) -> str:
        """"ça fait jouer l'ia grâce à la première meilleure évaluation de par la fonction minimax"""
        maxizingPlayer = True if self.turn == "White" else False
        valeur = self.minimax(1, maxizingPlayer, self.actual_game)
        for coup in self.coup_disponible():
            valeur_pour_chaque_coup = self.minimax(0, maxizingPlayer, self.actual_game)
            if valeur_pour_chaque_coup == valeur:
                return coup

    def coup_disponible(self, joueur: int, position : list[list[int]])->list[str]:

        coups_possibles = []
        
        couleur_ennemi = 1 if joueur == 2 else 2

        for x in range(8):
            for y in range(8):

                if joueur==position[x][y]:

                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            pion_possible = position[x+dx][y+dy]
                            if pion_possible == couleur_ennemi:
                                coordonnees = self.analyser_direction_pour_coups_possibles(x+dx,y+dy,couleur_ennemi,joueur,dx,dy,position)
                                if coordonnees is not None:
                                    en_str = self.coup_inverse[coordonnees[0]] + str(coordonnees[1])
                                    coups_possibles.append(en_str)

        return coups_possibles

    def analyser_direction_pour_coups_possibles(self, x: int, y: int, couleur : int, couleur_autre: int, dx: int, dy: int, position) -> tuple[int,int]:
        """Fonction récursive : 
        Retourne les coordonnées du prochain pion de la même couleur que celui entré en paramètre si il existe

        Args:
            x (int): coordonnées x d'un pion
            y (int): coordonnées y d'un pion
            couleur (int): couleur du pion dont on à les coordonnées
            couleur_autre (int): couleur opposée au pion dont on à les coordonnées
            dx (int): coordonées en x du vecteur direction
            dy (int): coordonées en y du vecteur direction

        Returns:
            tuple[int,int]: coordonnées du prochain pion de couleur adptée
        """
        print(x+dx, y+dy)
        if position[x+dx][y+dy] == 0:
            return (x+dx, y+dy)
        elif position[x+dx][y+dy] == couleur:
            return None
        return self.analyser_direction_pour_coups_possibles(x+dx, y+dy, couleur, couleur_autre, dx, dy, position)


    
    def compter_pions(self, position) -> tuple[int,int]:
        """
        Compte le nombre de pions de chaque joueur et le renvoie sous la forme d'un tuple.
        """
        pion_white = 0
        pion_black = 0
        for row in position:
            for pion in row:
                if pion == 1:
                    pion_white +=1
                elif pion == 2:
                    pion_black +=1
                else:
                    pass
        return (pion_white, pion_black)

    def colorier_entre(self, coo_x1 : int, coo_y1 :int, coo_x2 : int, coo_y2 : int, couleur : int, position):
        """Change la valeur des pions entre (x1; y1) et (x2; y2) de par les règles de l'Othello et grâce à des vecteurs
        """

        dx = int(coo_x2 - coo_x1) / abs((coo_x2 - coo_x1)) if (coo_x2 - coo_x1)!=0 else 0
        dy = int(coo_y2 - coo_y1) / abs((coo_y2 - coo_y1)) if (coo_y2 - coo_y1)!=0 else 0
        
        
        point_a_atteindre = (coo_x2, coo_y2)
        nouveau_point = (coo_x1, coo_y1)

        while nouveau_point != point_a_atteindre:
            position[nouveau_point[0]][nouveau_point[1]] = couleur
            nouveau_point = (int(nouveau_point[0]+dx), int(nouveau_point[1]+dy))
                
    def analyser_direction(self, x: int, y: int, couleur : int, couleur_autre: int, dx: int, dy: int, position) -> tuple[int,int]:
        """Fonction récursive : 
        Retourne les coordonnées du prochain pion de la même couleur que celui entré en paramètre si il existe

        Args:
            x (int): coordonnées x d'un pion
            y (int): coordonnées y d'un pion
            couleur (int): couleur du pion dont on à les coordonnées
            couleur_autre (int): couleur opposée au pion dont on à les coordonnées
            dx (int): coordonées en x du vecteur direction
            dy (int): coordonées en y du vecteur direction

        Returns:
            tuple[int,int]: coordonnées du prochain pion de couleur adptée
        """
        if position[x+dx][y+dy] == couleur:
            return (x+dx, y+dy)
        elif position[x+dx][y+dy] == 0:
            return None
        return self.analyser_direction(x+dx, y+dy, couleur, couleur_autre, dx, dy, position)

    def entre_pions(self, x: int, y: int, couleur : int, coul_ennemy : int, position):
        """
        Fonction qui effectue les vérificaitons nécéssaires afin de changer de couleur les pions aprés un tour
        """
        # Parcourir les directions
        for dx in range(-1,2):
            for dy in range(-1,2):
                

                pion_a_cote = position[x+dx][y+dy]

                if pion_a_cote == coul_ennemy:
                    dernier = self.analyser_direction(x, y, couleur, coul_ennemy, dx, dy, position)
                    print(f"{dernier=}")
                    if dernier is not None:
                        self.colorier_entre(x,y,dernier[0],dernier[1],couleur, position)


    def start(self):
        #S'occupe des évenements utilisateur
        while self.running:
            couleur_joueur = 2 if self.turn == "Black" else 1
            self.afficher_le_jeu(self.actual_game)
            coups_possible = self.coup_disponible(couleur_joueur, self.actual_game)
            if len(coups_possible) == 0:
                self.game_over = True
            print(f"C'est au tour du joueur : {self.turn}")
            print(f"Les coups possibles sont : {coups_possible}")
            
            # Demande à l'utilisateur d'entrer un coup
            self.move = input("Veuillez choisir une position pour jouer : \n- ")
            self.play_move(move=self.move, position=self.actual_game)  # Joue le coup choisi
            print(self.ia_joue())

    def play_move(self, move: str, position):
        ##Joue un coup donné sur un tableau de jeu donnée
        couleur_joueur = 2 if self.turn == "Black" else 1
        couleur_adversaire = 1 if self.turn == "Black" else 2
        coups_possibles = self.coup_disponible(couleur_joueur, self.actual_game)

        if bool(re.match(self.regex_coup_othello, move)):
            coup = [move[0], move[1]]
            if move in coups_possibles:
                if self.turn == "Black":
                    position[self.coup[coup[0]]][int(coup[1]) - 1] = 2
                    self.turn = "White"  # Change de joueur
                elif self.turn == "White":
                    position[self.coup[coup[0]]][int(coup[1]) - 1] = 1
                    self.turn = "Black"
                self.entre_pions(self.coup[coup[0]], int(coup[1]) - 1, couleur_joueur, couleur_adversaire, self.actual_game)
            else:
                print("Position Non Valide !")
        else:
            print("Position Non Valide !")

# Dimensions et paramètres du jeu

"""
WINDOWSIZE = 400
CELLSIZE = 50
ROW, COLUMN = 8
"""

# Démarrage du jeu
Game().start()
