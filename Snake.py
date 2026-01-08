"""
Snake Game - Version Python avec PyGame
Auteur : [Ton Nom]
Date : [Date]
"""

import pygame
import random
import sys
import time
from enum import Enum

# Initialisation PyGame
pygame.init()

# Constantes du jeu
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
TAILLE_CELLULE = 20
GRID_WIDTH = LARGEUR_ECRAN // TAILLE_CELLULE
GRID_HEIGHT = HAUTEUR_ECRAN // TAILLE_CELLULE
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
VERT_FONCE = (0, 200, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 120, 255)
JAUNE = (255, 255, 0)
VIOLET = (180, 0, 255)
GRIS = (40, 40, 40)
GRIS_CLAIR = (100, 100, 100)

# Désactiver les sons pour éviter les problèmes
son_manger = None
son_game_over = None

class Direction(Enum):
    """Directions possibles pour le serpent"""
    HAUT = (0, -1)
    BAS = (0, 1)
    GAUCHE = (-1, 0)
    DROITE = (1, 0)

class Niveau(Enum):
    """Niveaux de difficulté"""
    FACILE = 1
    MOYEN = 2
    DIFFICILE = 3
    EXTREME = 4

class Serpent:
    """Classe qui représente le serpent"""
    
    def __init__(self, x=None, y=None):
        # Position initiale (centre de l'écran par défaut)
        if x is None:
            x = GRID_WIDTH // 2
        if y is None:
            y = GRID_HEIGHT // 2
            
        self.corps = [(x, y)]  # Liste de tuples (x, y)
        self.direction = Direction.DROITE
        self.nouvelle_direction = Direction.DROITE
        self.couleur_tete = VERT
        self.couleur_corps = VERT_FONCE
        self.grandir_prochain_mouvement = False
        self.vitesse = 10  # Cases par seconde
        self.temps_dernier_mouvement = 0
        self.score = 0
        self.vies = 3
        self.est_invincible = False
        self.temps_invincibilite = 0
        
    def changer_direction(self, nouvelle_direction):
        """Change la direction du serpent (avec vérification pour éviter les demi-tours)"""
        # Empêcher le demi-tour direct
        if (nouvelle_direction == Direction.HAUT and self.direction != Direction.BAS) or \
           (nouvelle_direction == Direction.BAS and self.direction != Direction.HAUT) or \
           (nouvelle_direction == Direction.GAUCHE and self.direction != Direction.DROITE) or \
           (nouvelle_direction == Direction.DROITE and self.direction != Direction.GAUCHE):
            self.nouvelle_direction = nouvelle_direction
    
    def bouger(self, temps_actuel):
        """Déplace le serpent selon sa vitesse"""
        # Vérifier si c'est le moment de bouger
        if temps_actuel - self.temps_dernier_mouvement < 1.0 / self.vitesse:
            return False
            
        self.temps_dernier_mouvement = temps_actuel
        self.direction = self.nouvelle_direction
        
        # Obtenir la position actuelle de la tête
        tete_x, tete_y = self.corps[0]
        
        # Calculer la nouvelle position
        dx, dy = self.direction.value
        nouvelle_tete = ((tete_x + dx) % GRID_WIDTH, (tete_y + dy) % GRID_HEIGHT)
        
        # Ajouter la nouvelle tête
        self.corps.insert(0, nouvelle_tete)
        
        # Retirer la queue si le serpent ne doit pas grandir
        if not self.grandir_prochain_mouvement:
            self.corps.pop()
        else:
            self.grandir_prochain_mouvement = False
            
        return True
    
    def grandir(self):
        """Le serpent grandira au prochain mouvement"""
        self.grandir_prochain_mouvement = True
        self.score += 10
        
        # Augmenter légèrement la vitesse tous les 5 points
        if self.score % 50 == 0:
            self.vitesse = min(self.vitesse + 1, 20)
    
    def check_collision_corps(self):
        """Vérifie si la tête touche le corps"""
        if len(self.corps) > 1 and self.corps[0] in self.corps[1:]:
            return True
        return False
    
    def check_collision_mur(self, murs):
        """Vérifie si la tête touche un mur"""
        tete_x, tete_y = self.corps[0]
        if (tete_x, tete_y) in murs:
            return True
        return False
    
    def perdre_vie(self):
        """Le serpent perd une vie"""
        if not self.est_invincible:
            self.vies -= 1
            self.est_invincible = True
            self.temps_invincibilite = time.time() + 2  # 2 secondes d'invincibilité
            return True
        return False
    
    def update_invincibilite(self):
        """Met à jour l'état d'invincibilité"""
        if self.est_invincible and time.time() > self.temps_invincibilite:
            self.est_invincible = False
    
    def reset(self):
        """Réinitialise le serpent (après une vie perdue)"""
        x = GRID_WIDTH // 2
        y = GRID_HEIGHT // 2
        self.corps = [(x, y)]
        self.direction = Direction.DROITE
        self.nouvelle_direction = Direction.DROITE
        self.grandir_prochain_mouvement = False
        self.est_invincible = True
        self.temps_invincibilite = time.time() + 2
    
    def dessiner(self, ecran):
        """Dessine le serpent sur l'écran"""
        for i, (x, y) in enumerate(self.corps):
            # Calculer les coordonnées en pixels
            rect_x = x * TAILLE_CELLULE
            rect_y = y * TAILLE_CELLULE
            
            # Choisir la couleur (tête différente du corps)
            couleur = self.couleur_tete if i == 0 else self.couleur_corps
            
            # Si invincible, faire clignoter
            if self.est_invincible and i == 0:
                if int(time.time() * 10) % 2 == 0:  # Clignotement rapide
                    couleur = BLANC
            
            # Dessiner le segment
            pygame.draw.rect(ecran, couleur, 
                            (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE))
            
            # Dessiner les yeux sur la tête
            if i == 0:
                self.dessiner_yeux(ecran, rect_x, rect_y)
            
            # Dessiner un léger contour
            pygame.draw.rect(ecran, NOIR, 
                            (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE), 1)
    
    def dessiner_yeux(self, ecran, x, y):
        """Dessine les yeux du serpent selon la direction"""
        taille_oeil = TAILLE_CELLULE // 5
        offset = TAILLE_CELLULE // 3
        
        # Position des yeux selon la direction
        if self.direction == Direction.DROITE:
            oeil1 = (x + TAILLE_CELLULE - offset, y + offset)
            oeil2 = (x + TAILLE_CELLULE - offset, y + TAILLE_CELLULE - offset)
        elif self.direction == Direction.GAUCHE:
            oeil1 = (x + offset, y + offset)
            oeil2 = (x + offset, y + TAILLE_CELLULE - offset)
        elif self.direction == Direction.HAUT:
            oeil1 = (x + offset, y + offset)
            oeil2 = (x + TAILLE_CELLULE - offset, y + offset)
        else:  # BAS
            oeil1 = (x + offset, y + TAILLE_CELLULE - offset)
            oeil2 = (x + TAILLE_CELLULE - offset, y + TAILLE_CELLULE - offset)
        
        # Dessiner les yeux
        pygame.draw.circle(ecran, NOIR, oeil1, taille_oeil)
        pygame.draw.circle(ecran, NOIR, oeil2, taille_oeil)

class Nourriture:
    """Classe qui représente la nourriture (pomme)"""
    
    def __init__(self):
        # Types spéciaux de nourriture (DOIT ÊTRE DÉFINI EN PREMIER !)
        self.types_speciaux = {
            "normal": {"couleur": ROUGE, "points": 10, "duree": 0},
            "special": {"couleur": JAUNE, "points": 30, "duree": 10},
            "poison": {"couleur": VIOLET, "points": -20, "duree": 15},
            "vie": {"couleur": BLEU, "points": 0, "duree": 8}
        }
        
        self.position = (0, 0)
        self.couleur = ROUGE
        self.type_nourriture = "normal"
        self.temps_apparition = 0
        self.duree_vie = 0
        self.regenerer_position()
        
    def regenerer_position(self, serpent=None, murs=None, nourritures_speciales=None):
        """Génère une nouvelle position aléatoire pour la nourriture"""
        if serpent is None:
            serpent_corps = []
        else:
            serpent_corps = serpent.corps
            
        if murs is None:
            murs = []
            
        if nourritures_speciales is None:
            nourritures_speciales = []
        
        # Liste des positions occupées
        positions_occupees = set(serpent_corps + murs)
        for nourriture in nourritures_speciales:
            positions_occupees.add(nourriture.position)
        
        # Générer jusqu'à trouver une position libre
        essais = 0
        while essais < 100:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if (x, y) not in positions_occupees:
                self.position = (x, y)
                
                # Déterminer le type de nourriture
                rand = random.random()
                if rand < 0.05:  # 5% poison
                    self.changer_type("poison")
                elif rand < 0.15:  # 10% spécial
                    self.changer_type("special")
                elif rand < 0.20:  # 5% vie
                    self.changer_type("vie")
                else:  # 80% normal
                    self.changer_type("normal")
                    
                self.temps_apparition = time.time()
                return True
                
            essais += 1
        
        return False
    
    def changer_type(self, type_nourriture):
        """Change le type de nourriture"""
        self.type_nourriture = type_nourriture
        type_info = self.types_speciaux.get(type_nourriture, self.types_speciaux["normal"])
        self.couleur = type_info["couleur"]
        self.duree_vie = type_info["duree"]
    
    def est_expiree(self):
        """Vérifie si la nourriture spéciale a expiré"""
        if self.duree_vie > 0:
            return time.time() - self.temps_apparition > self.duree_vie
        return False
    
    def manger(self, serpent):
        """Effet quand le serpent mange cette nourriture"""
        type_info = self.types_speciaux.get(self.type_nourriture, self.types_speciaux["normal"])
        points = type_info["points"]
        
        if self.type_nourriture == "vie":
            serpent.vies = min(serpent.vies + 1, 5)
            return 0
        elif self.type_nourriture == "poison":
            if serpent.perdre_vie():
                return points
            return 0
        else:
            serpent.grandir()
            return points
    
    def dessiner(self, ecran):
        """Dessine la nourriture sur l'écran"""
        x, y = self.position
        rect_x = x * TAILLE_CELLULE
        rect_y = y * TAILLE_CELLULE
        
        # Dessiner la nourriture
        pygame.draw.rect(ecran, self.couleur, 
                        (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE))
        
        # Dessiner un contour
        pygame.draw.rect(ecran, NOIR, 
                        (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE), 1)

class JeuSnake:
    """Classe principale du jeu Snake"""
    
    def __init__(self):
        # Initialisation de l'écran
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption("Snake Game - Python Edition")
        self.horloge = pygame.time.Clock()
        
        # Polices
        self.police_grande = pygame.font.Font(None, 48)
        self.police_moyenne = pygame.font.Font(None, 36)
        self.police_petite = pygame.font.Font(None, 24)
        
        # État du jeu
        self.etat = "MENU"
        self.niveau = Niveau.MOYEN
        self.serpent = None
        self.nourriture = None
        self.nourritures_speciales = []
        self.murs = []
        self.score = 0
        self.high_score = 0
        self.temps_debut = 0
        self.temps_jeu = 0
        
        # Pas de musique pour éviter les problèmes
        self.musique_active = False
        
        # Initialiser les éléments du jeu
        self.initialiser_jeu()
    
    def initialiser_jeu(self):
        """Initialise ou réinitialise le jeu"""
        self.serpent = Serpent()
        self.nourriture = Nourriture()
        self.nourritures_speciales = []
        self.murs = []
        self.score = 0
        self.temps_debut = time.time()
        
        # Configurer selon le niveau
        if self.niveau == Niveau.FACILE:
            self.serpent.vitesse = 8
            self.serpent.vies = 5
        elif self.niveau == Niveau.MOYEN:
            self.serpent.vitesse = 10
            self.serpent.vies = 3
            self.generer_murs(5)
        elif self.niveau == Niveau.DIFFICILE:
            self.serpent.vitesse = 12
            self.serpent.vies = 2
            self.generer_murs(10)
        else:  # EXTREME
            self.serpent.vitesse = 15
            self.serpent.vies = 1
            self.generer_murs(15)
        
        # Positionner la nourriture
        self.nourriture.regenerer_position(self.serpent, self.murs, self.nourritures_speciales)
    
    def generer_murs(self, nombre):
        """Génère des murs aléatoires"""
        for _ in range(nombre):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                
                # Éviter de placer un mur sur le serpent ou la nourriture
                if (x, y) != self.serpent.corps[0] and (x, y) != self.nourriture.position:
                    self.murs.append((x, y))
                    break
    
    def gerer_evenements(self):
        """Gère tous les événements du jeu"""
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            
            elif evenement.type == pygame.KEYDOWN:
                if self.etat == "MENU":
                    self.gerer_evenements_menu(evenement)
                elif self.etat == "JEU":
                    self.gerer_evenements_jeu(evenement)
                elif self.etat == "GAME_OVER":
                    self.gerer_evenements_game_over(evenement)
                elif self.etat == "PAUSE":
                    self.gerer_evenements_pause(evenement)
        
        return True
    
    def gerer_evenements_menu(self, evenement):
        """Gère les événements dans le menu"""
        if evenement.key == pygame.K_1:
            self.niveau = Niveau.FACILE
            self.etat = "JEU"
            self.initialiser_jeu()
        elif evenement.key == pygame.K_2:
            self.niveau = Niveau.MOYEN
            self.etat = "JEU"
            self.initialiser_jeu()
        elif evenement.key == pygame.K_3:
            self.niveau = Niveau.DIFFICILE
            self.etat = "JEU"
            self.initialiser_jeu()
        elif evenement.key == pygame.K_4:
            self.niveau = Niveau.EXTREME
            self.etat = "JEU"
            self.initialiser_jeu()
        elif evenement.key == pygame.K_ESCAPE:
            return False
    
    def gerer_evenements_jeu(self, evenement):
        """Gère les événements pendant le jeu"""
        if evenement.key == pygame.K_UP:
            self.serpent.changer_direction(Direction.HAUT)
        elif evenement.key == pygame.K_DOWN:
            self.serpent.changer_direction(Direction.BAS)
        elif evenement.key == pygame.K_LEFT:
            self.serpent.changer_direction(Direction.GAUCHE)
        elif evenement.key == pygame.K_RIGHT:
            self.serpent.changer_direction(Direction.DROITE)
        elif evenement.key == pygame.K_p:
            self.etat = "PAUSE"
        elif evenement.key == pygame.K_ESCAPE:
            self.etat = "MENU"
    
    def gerer_evenements_game_over(self, evenement):
        """Gère les événements à l'écran de game over"""
        if evenement.key == pygame.K_r:
            self.etat = "JEU"
            self.initialiser_jeu()
        elif evenement.key == pygame.K_m:
            self.etat = "MENU"
        elif evenement.key == pygame.K_ESCAPE:
            return False
    
    def gerer_evenements_pause(self, evenement):
        """Gère les événements en pause"""
        if evenement.key == pygame.K_p or evenement.key == pygame.K_ESCAPE:
            self.etat = "JEU"
    
    def mettre_a_jour(self):
        """Met à jour la logique du jeu"""
        if self.etat != "JEU":
            return
        
        temps_actuel = time.time()
        self.temps_jeu = temps_actuel - self.temps_debut
        
        # Mettre à jour l'invincibilité du serpent
        self.serpent.update_invincibilite()
        
        # Déplacer le serpent
        if self.serpent.bouger(temps_actuel):
            # Vérifier les collisions avec la nourriture
            if self.serpent.corps[0] == self.nourriture.position:
                # Manger la nourriture
                points = self.nourriture.manger(self.serpent)
                self.score += max(0, points)
                
                # Régénérer la nourriture
                self.nourriture.regenerer_position(self.serpent, self.murs, self.nourritures_speciales)
            
            # Vérifier les collisions avec le corps
            if self.serpent.check_collision_corps():
                if self.serpent.perdre_vie():
                    pass
            
            # Vérifier les collisions avec les murs
            if self.serpent.check_collision_mur(self.murs):
                if self.serpent.perdre_vie():
                    pass
            
            # Vérifier si le serpent n'a plus de vies
            if self.serpent.vies <= 0:
                self.etat = "GAME_OVER"
                
                # Mettre à jour le high score
                if self.score > self.high_score:
                    self.high_score = self.score
    
    def dessiner(self):
        """Dessine tout l'écran"""
        # Fond
        self.ecran.fill(NOIR)
        
        # Dessiner la grille
        self.dessiner_grille()
        
        if self.etat == "MENU":
            self.dessiner_menu()
        elif self.etat == "JEU":
            self.dessiner_jeu()
        elif self.etat == "GAME_OVER":
            self.dessiner_jeu()
            self.dessiner_game_over()
        elif self.etat == "PAUSE":
            self.dessiner_jeu()
            self.dessiner_pause()
        
        # Mettre à jour l'affichage
        pygame.display.flip()
    
    def dessiner_grille(self):
        """Dessine une grille discrète en fond"""
        for x in range(0, LARGEUR_ECRAN, TAILLE_CELLULE):
            pygame.draw.line(self.ecran, GRIS, (x, 0), (x, HAUTEUR_ECRAN), 1)
        for y in range(0, HAUTEUR_ECRAN, TAILLE_CELLULE):
            pygame.draw.line(self.ecran, GRIS, (0, y), (LARGEUR_ECRAN, y), 1)
    
    def dessiner_menu(self):
        """Dessine l'écran de menu"""
        # Titre
        titre = self.police_grande.render("SNAKE GAME", True, VERT)
        self.ecran.blit(titre, (LARGEUR_ECRAN // 2 - titre.get_width() // 2, 50))
        
        # Sous-titre
        sous_titre = self.police_petite.render("Python Edition", True, BLANC)
        self.ecran.blit(sous_titre, (LARGEUR_ECRAN // 2 - sous_titre.get_width() // 2, 110))
        
        # Options
        options_y = 200
        espacement = 50
        
        niveaux = [
            ("1. FACILE", "Vitesse lente, 5 vies, pas de murs", VERT),
            ("2. MOYEN", "Vitesse normale, 3 vies, quelques murs", JAUNE),
            ("3. DIFFICILE", "Vitesse rapide, 2 vies, beaucoup de murs", (255, 165, 0)),
            ("4. EXTRÊME", "Vitesse très rapide, 1 vie, nombreux murs", ROUGE)
        ]
        
        for niveau, description, couleur in niveaux:
            texte_niveau = self.police_moyenne.render(niveau, True, couleur)
            self.ecran.blit(texte_niveau, (100, options_y))
            
            texte_desc = self.police_petite.render(description, True, BLANC)
            self.ecran.blit(texte_desc, (150, options_y + 30))
            
            options_y += espacement
        
        # Contrôles
        controles_y = 450
        controles = [
            "Appuyez sur 1, 2, 3 ou 4 pour choisir le niveau",
            "ESC: Quitter le menu"
        ]
        
        for i, controle in enumerate(controles):
            texte = self.police_petite.render(controle, True, GRIS_CLAIR)
            self.ecran.blit(texte, (LARGEUR_ECRAN // 2 - texte.get_width() // 2, controles_y + i * 30))
    
    def dessiner_jeu(self):
        """Dessine l'écran de jeu"""
        # Dessiner les murs
        for x, y in self.murs:
            rect_x = x * TAILLE_CELLULE
            rect_y = y * TAILLE_CELLULE
            pygame.draw.rect(self.ecran, GRIS_CLAIR, 
                            (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE))
            pygame.draw.rect(self.ecran, NOIR, 
                            (rect_x, rect_y, TAILLE_CELLULE, TAILLE_CELLULE), 1)
        
        # Dessiner la nourriture
        self.nourriture.dessiner(self.ecran)
        
        # Dessiner le serpent
        self.serpent.dessiner(self.ecran)
        
        # Dessiner l'interface
        self.dessiner_interface()
    
    def dessiner_interface(self):
        """Dessine l'interface utilisateur pendant le jeu"""
        # Score
        score_texte = self.police_moyenne.render(f"Score: {self.score}", True, BLANC)
        self.ecran.blit(score_texte, (10, 10))
        
        # High Score
        high_score_texte = self.police_petite.render(f"High Score: {self.high_score}", True, JAUNE)
        self.ecran.blit(high_score_texte, (10, 50))
        
        # Vies
        vies_texte = self.police_moyenne.render(f"Vies: {self.serpent.vies}", True, ROUGE)
        self.ecran.blit(vies_texte, (LARGEUR_ECRAN - 120, 10))
        
        # Niveau
        niveau_texte = self.police_petite.render(f"Niveau: {self.niveau.name}", True, VERT)
        self.ecran.blit(niveau_texte, (LARGEUR_ECRAN - 120, 50))
        
        # Temps
        temps_texte = self.police_petite.render(f"Temps: {int(self.temps_jeu)}s", True, BLANC)
        self.ecran.blit(temps_texte, (LARGEUR_ECRAN // 2 - temps_texte.get_width() // 2, 10))
        
        # Instructions
        instructions = [
            "Flèches: Déplacer",
            "P: Pause",
            "ESC: Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            texte = self.police_petite.render(instruction, True, GRIS_CLAIR)
            self.ecran.blit(texte, (10, HAUTEUR_ECRAN - 100 + i * 25))
    
    def dessiner_game_over(self):
        """Dessine l'écran de game over par-dessus le jeu"""
        # Semi-transparence
        overlay = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ecran.blit(overlay, (0, 0))
        
        # Texte GAME OVER
        game_over = self.police_grande.render("GAME OVER", True, ROUGE)
        self.ecran.blit(game_over, (LARGEUR_ECRAN // 2 - game_over.get_width() // 2, 150))
        
        # Score final
        score_texte = self.police_moyenne.render(f"Score final: {self.score}", True, BLANC)
        self.ecran.blit(score_texte, (LARGEUR_ECRAN // 2 - score_texte.get_width() // 2, 220))
        
        # High Score
        if self.score == self.high_score:
            high_score_texte = self.police_moyenne.render("NOUVEAU HIGH SCORE!", True, JAUNE)
            self.ecran.blit(high_score_texte, (LARGEUR_ECRAN // 2 - high_score_texte.get_width() // 2, 260))
        else:
            high_score_texte = self.police_moyenne.render(f"High Score: {self.high_score}", True, JAUNE)
            self.ecran.blit(high_score_texte, (LARGEUR_ECRAN // 2 - high_score_texte.get_width() // 2, 260))
        
        # Options
        options_y = 320
        options = [
            "R: Rejouer",
            "M: Retour au menu",
            "ESC: Quitter"
        ]
        
        for i, option in enumerate(options):
            texte = self.police_moyenne.render(option, True, VERT)
            self.ecran.blit(texte, (LARGEUR_ECRAN // 2 - texte.get_width() // 2, options_y + i * 50))
    
    def dessiner_pause(self):
        """Dessine l'écran de pause par-dessus le jeu"""
        # Semi-transparence
        overlay = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ecran.blit(overlay, (0, 0))
        
        # Texte PAUSE
        pause = self.police_grande.render("PAUSE", True, JAUNE)
        self.ecran.blit(pause, (LARGEUR_ECRAN // 2 - pause.get_width() // 2, 200))
        
        # Instructions
        instructions = [
            "Appuyez sur P pour reprendre",
            "ESC pour retourner au menu"
        ]
        
        for i, instruction in enumerate(instructions):
            texte = self.police_moyenne.render(instruction, True, BLANC)
            self.ecran.blit(texte, (LARGEUR_ECRAN // 2 - texte.get_width() // 2, 280 + i * 40))
    
    def executer(self):
        """Boucle principale du jeu"""
        en_cours = True
        
        while en_cours:
            # Gérer les événements
            en_cours = self.gerer_evenements()
            
            # Mettre à jour la logique du jeu
            self.mettre_a_jour()
            
            # Dessiner l'écran
            self.dessiner()
            
            # Contrôler le FPS
            self.horloge.tick(FPS)
        
        # Quitter PyGame
        pygame.quit()
        sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    jeu = JeuSnake()
    jeu.executer()