import pyxel
import re

class Game:
    def __init__(self) -> None:
        # Dictionnaire pour associer des couleurs à leurs codes
        self.couleur = {0: "Vide", 1: "Blanc", 2: "Noir"}
        
        # Dictionnaire pour convertir les lettres (colonnes) en indices numériques
        self.coup = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        
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

    def afficher_le_jeu(self):
        # Affiche la grille de jeu actuelle en console
        ligne = ""
        for i in self.actual_game:
            for j in i:
                ligne += str(j)
            print(ligne)
            ligne = ""

    def coup_disponible(self) -> list[str]:
        # Renvoie une liste des coups possibles pour le joueur actuel
        moves_possible = []
        
        # Détermine la couleur du joueur et de l'ennemi
        couleur_joueur = 2 if self.turn == "Black" else 1
        couleur_ennemi = 1 if self.turn == "Black" else 2

        # Parcours de la grille pour trouver des pions du joueur
        for i in range(8):
            for j in range(8):
                if self.actual_game[i][j] == couleur_joueur:

                    # Vérification dans toutes les directions
                    for k in range(-1, 2):
                        for n in range(-1, 2): 
                            if k == 0 and n == 0:
                                continue

                            # Ceci représente les cases possibles avec leur absices étant x et y leur ordonnée
                            x = i +k
                            y = j + n
                            
                            if 0 <=x< 8 and 0 <=y< 8 and self.actual_game[x][y] == couleur_ennemi: # SI  x est compris entre 0 et 8 ET y est compris entre 0 et 8 et (t) case autour des cases alliés est enemie :
                                while 0 <=x<8 and 0 <=y<8: # Tant que x et y sont entre 0 et 8 :
                                    x += k
                                    y += n
                                    if not 0 <=x<8 and 0<=y<8: # Si il n'est pas compris dans le tableau:
                                        break
                                    if self.actual_game[x][y] == 0:
                                        coup_possible = str(self.coup_inverse[x]) + str(y + 1)
                                        if coup_possible not in moves_possible:
                                            moves_possible.append(coup_possible)
                                        break
                                    if self.actual_game[x][y] == couleur_joueur:
                                        break
                                    print(moves_possible)
        return moves_possible
    
    def flippeur(self):
        ...

    def start(self):
        # Boucle principale du jeu
        while self.running:
            self.afficher_le_jeu()  # Affiche la grille actuelle
            coups_possible = self.coup_disponible()
            print(f"C'est au tour du joueur : {self.turn}")
            print(f"Les coups possibles sont : {coups_possible}")
            
            # Demande à l'utilisateur d'entrer un coup
            move = input("Veuillez choisir une position pour jouer : \n- ")
            self.play_move(move=move)  # Joue le coup choisi

    def play_move(self, move: str):
        # Joue le coup donné par le joueur
        couleur_joueur = 2 if self.turn == "Black" else 1
        couleur_adversaire = 1 if self.turn == "Black" else 2
        coups_possibles = self.coup_disponible()
        
        # Vérifie si le coup est valide avec l'expression régulière
        if bool(re.match(self.regex_coup_othello, move)):
            coup = [move[0], move[1]]
            if move in coups_possibles:
                # Met à jour la grille avec le coup du joueur
                if self.turn == "Black":
                    self.actual_game[self.coup[coup[0]]][int(coup[1]) - 1] = 2
                    self.turn = "White"  # Change de joueur
                elif self.turn == "White":
                    self.actual_game[self.coup[coup[0]]][int(coup[1]) - 1] = 1
                    self.turn = "Black"
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
