from fltk import *
from random import randint
import math
import os
import random
from classement import *

# --- CONSTANTES DE CONFIGURATION ---
TAILLE_PIXEL_CASE = 50
MARGE_PIXEL_X = 100
MARGE_PIXEL_Y = 100
NOMBRE_LIGNES = 10
NOMBRE_COLONNES = 8
POSITION_X_RATELIER = 550 # Position X des cases supplémentaires
POSITION_Y_RATELIER_DEPART = 100 # Position Y de départ du râtelier

# --- Mapping Couleur -> Forme pour le mode Daltonien ---
MAP_COULEUR_FORME = {
    'red': 'cercle',
    'blue': 'carre',
    'green': 'triangle',
    'yellow': 'etoile',
    'purple': 'losange'  # Ajout pour le mode Difficile
}

# --- FONCTIONS UTILITAIRES ---
def indices_vers_pixels(indice_ligne, indice_colonne):
    """Convertit indices grille -> coordonnées pixels (coin haut-gauche)"""
    coordonnee_x = MARGE_PIXEL_X + indice_colonne * TAILLE_PIXEL_CASE
    coordonnee_y = MARGE_PIXEL_Y + indice_ligne * TAILLE_PIXEL_CASE
    return coordonnee_x, coordonnee_y

def pixels_vers_indices(coordonnee_x_clic, coordonnee_y_clic):
    """Convertit clic souris -> indices grille. Retourne None si hors plateau."""
    limite_x_min = MARGE_PIXEL_X
    limite_x_max = MARGE_PIXEL_X + NOMBRE_COLONNES * TAILLE_PIXEL_CASE
    limite_y_min = MARGE_PIXEL_Y
    limite_y_max = MARGE_PIXEL_Y + NOMBRE_LIGNES * TAILLE_PIXEL_CASE
    if not (limite_x_min <= coordonnee_x_clic < limite_x_max and 
            limite_y_min <= coordonnee_y_clic < limite_y_max):
        return None, None
    indice_colonne = (coordonnee_x_clic - MARGE_PIXEL_X) // TAILLE_PIXEL_CASE
    indice_ligne = (coordonnee_y_clic - MARGE_PIXEL_Y) // TAILLE_PIXEL_CASE
    return indice_ligne, indice_colonne

# --- NOUVELLE FONCTION POUR GÉRER L'AFFICHAGE DU FOND PERSONNALISÉ ---
def dessiner_fond_personnalise(mode_jeu, largeur_fenetre=1200, hauteur_fenetre=750):
    """
    Sélectionne aléatoirement une image de fond du dossier approprié et l'affiche.
    """
    dossier_base = "fond_ecran"
    if mode_jeu == 'SOLO':
        dossier = os.path.join(dossier_base, "Mode_SOLO")
    elif mode_jeu == 'VS':
        dossier = os.path.join(dossier_base, "Mode_MULTI")
    else:
        rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage='grey', couleur='grey')
        return
    try:
        fichiers = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not fichiers:
            print("Attention: Aucun fichier image trouvé dans " + str(dossier) + ". Utilisation d'un fond gris.")
            rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage='grey', couleur='grey')
            return
        fichier_choisi = os.path.join(dossier, random.choice(fichiers))
        image(600 ,375 ,fichier_choisi , ancrage='center' , largeur=1200, hauteur=750)
    except FileNotFoundError:
        print("Erreur: Dossier" + str(dossier) + " non trouvé. Assurez-vous qu'il existe. Utilisation d'un fond gris.")
        rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage='grey', couleur='grey')
    except Exception as e:
        print("Erreur lors du chargement de l'image " + str(fichier_choisi) + ":" + str(e) + ". Utilisation d'un fond gris.")
        rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage='grey', couleur='grey')

# --- DESSIN ET GRAPHIQUE ---
def dessiner_jeton_centre(x_centre, y_centre, type_jeton, couleur_jeton, mode_daltonien=False):
    """Dessine un jeton à partir de son centre, avec une forme si mode_daltonien est True."""
    rayon_exterieur = 20
    rayon_interieur = 10
    taille_forme_base = 20 
    if type_jeton == 1:
        cercle(x_centre, y_centre, rayon_exterieur, couleur='black', remplissage=couleur_jeton)
    elif type_jeton == 2:
        cercle(x_centre, y_centre, rayon_exterieur, couleur='black')
        cercle(x_centre, y_centre, rayon_interieur, couleur='black', remplissage=couleur_jeton)
    else:
        return
    if mode_daltonien and couleur_jeton in MAP_COULEUR_FORME:
        forme = MAP_COULEUR_FORME[couleur_jeton]
        couleur_forme = 'black'
        if type_jeton == 1:
            taille_forme = taille_forme_base
        else:
            taille_forme = taille_forme_base * 0.7 
        if forme == 'cercle':
            cercle(x_centre, y_centre, taille_forme * 0.5, couleur=couleur_forme, remplissage=couleur_forme)
        elif forme == 'carre':
            demi_taille = int((taille_forme * 0.9) // 2)
            rectangle(x_centre - demi_taille, y_centre - demi_taille, 
                      x_centre + demi_taille, y_centre + demi_taille, 
                      couleur=couleur_forme, remplissage=couleur_forme)
        elif forme == 'triangle':
            taille_tri = taille_forme * 0.9
            polygone([(x_centre, y_centre - taille_tri), 
                      (x_centre - int(taille_tri * 0.866), y_centre + int(taille_tri * 0.5)), 
                      (x_centre + int(taille_tri * 0.866), y_centre + int(taille_tri * 0.5))], 
                     couleur=couleur_forme, remplissage=couleur_forme)
        elif forme == 'etoile':
            taille_etoile = taille_forme * 0.9
            rayon_externe = taille_etoile
            rayon_interne = taille_etoile * 0.4 
            points = []
            for i in range(10):
                angle_deg = i * 36
                angle_rad = math.radians(angle_deg - 90) 
                r = rayon_externe if i % 2 == 0 else rayon_interne
                x = x_centre + int(r * math.cos(angle_rad))
                y = y_centre + int(r * math.sin(angle_rad))
                points.append((x, y))
            polygone(points, couleur=couleur_forme, remplissage=couleur_forme)
        elif forme == 'losange': # Ajout Losange pour le mode Difficile
            t = taille_forme * 0.9
            polygone([(x_centre, y_centre - t), (x_centre + t, y_centre), 
                      (x_centre, y_centre + t), (x_centre - t, y_centre)], 
                     couleur=couleur_forme, remplissage=couleur_forme)

def dessiner_case(indice_ligne, indice_colonne, type_case, couleur_jeton='white', mode_daltonien=False):
    """Dessine une case du plateau principal (mise à jour pour le mode daltonien)"""
    x_coin, y_coin = indices_vers_pixels(indice_ligne, indice_colonne)
    if type_case == 0:
        couleur_remplissage = 'black'
    elif type_case == 4:
        couleur_remplissage = 'white'
    else:
        couleur_remplissage = 'white'
    rectangle(x_coin, y_coin, x_coin + TAILLE_PIXEL_CASE, y_coin + TAILLE_PIXEL_CASE, remplissage=couleur_remplissage, couleur='black')
    if type_case in [1, 2]:
        dessiner_jeton_centre(x_coin + 25, y_coin + 25, type_case, couleur_jeton, mode_daltonien)

def dessiner_ratelier(etat_cases_suppl, mode_daltonien=False):
    """Redessine toute la zone des cases supplémentaires (mise à jour pour le mode daltonien)"""
    rectangle(POSITION_X_RATELIER - 10, POSITION_Y_RATELIER_DEPART - 10, POSITION_X_RATELIER + 60, POSITION_Y_RATELIER_DEPART + 260, remplissage='white', couleur='white')
    y_actuel = POSITION_Y_RATELIER_DEPART
    for i in range(5):
        couleur_jeton = etat_cases_suppl[i]
        rectangle(POSITION_X_RATELIER, y_actuel, POSITION_X_RATELIER + 50, y_actuel + 50, remplissage='white', couleur='black')
        if couleur_jeton is not None:
            dessiner_jeton_centre(POSITION_X_RATELIER + 25, y_actuel + 25, 1, couleur_jeton, mode_daltonien) 
        y_actuel += 50

def rafraichir_plateau_entier(plan_jeu, dictionnaire_couleurs, mode_daltonien=False):
    """Redessine tout le plateau (mise à jour pour le mode daltonien)"""
    rectangle(MARGE_PIXEL_X-5, MARGE_PIXEL_Y-5, MARGE_PIXEL_X + NOMBRE_COLONNES*TAILLE_PIXEL_CASE + 5, 
              MARGE_PIXEL_Y + NOMBRE_LIGNES*TAILLE_PIXEL_CASE + 5, couleur='white', remplissage='white')
    for indice_ligne in range(len(plan_jeu)):
        for indice_colonne in range(len(plan_jeu[0])):
            couleur = dictionnaire_couleurs.get((indice_ligne, indice_colonne), 'white')
            dessiner_case(indice_ligne, indice_colonne, plan_jeu[indice_ligne][indice_colonne], couleur, mode_daltonien)

# --- LOGIQUE DU JEU ---
def generer_plan_plateau():
    plan_plateau = []
    for indice_ligne in range(NOMBRE_LIGNES):
        ligne_nouvelle = []
        for indice_colonne in range(NOMBRE_COLONNES):
            if randint(0, 3) == 3: # Probabilité d'un mur (type 0)
                ligne_nouvelle.append(0) # Mur
            elif indice_ligne == 0: # Première ligne = gros jetons (type 1)
                ligne_nouvelle.append(1)
            else: # Autres = petits jetons (type 2)
                ligne_nouvelle.append(2)
        plan_plateau.append(ligne_nouvelle)
    return plan_plateau

def calculer_total_jeton(plan_jeu) :
    compteur = 0
    for ligne in plan_jeu :
        for case in ligne :
            if case in [1 , 2] :
                compteur += 1
    return compteur

def trouver_point_depart(plan_jeu):
    ligne_depart = 0
    if len(plan_jeu) == 0 or len(plan_jeu[0]) == 0:
        return None, None 
    nb_colonnes = len(plan_jeu[0])
    for c in range(nb_colonnes):
        if plan_jeu[ligne_depart][c] in [1, 2]: 
            return ligne_depart, c
    return None, None

def parcours_profondeur(plan_jeu, ligne, colonne, visitees , nb_lignes , nb_colonnes) :
    if ligne < 0 or ligne >= nb_lignes or colonne < 0 or colonne >= nb_colonnes :
        return
    if plan_jeu[ligne][colonne] == 0 :
        return
    if (ligne,colonne) in visitees :
        return
    visitees.append((ligne,colonne))
    deplacement = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for mouvement in deplacement :
        nouveau_ligne = ligne + mouvement[0]
        nouveau_colonne = colonne + mouvement[1]
        parcours_profondeur(plan_jeu , nouveau_ligne , nouveau_colonne , visitees , nb_lignes , nb_colonnes)
    return 

def corriger_isolations(plan_jeu):
    while True:
        nb_lignes = len(plan_jeu)
        nb_colonnes = len(plan_jeu[0])
        total_jetons = calculer_total_jeton(plan_jeu)
        if total_jetons == 0:
            return plan_jeu 
        depart_ligne, depart_colonne = trouver_point_depart(plan_jeu)
        if depart_ligne is None:
            mur_cassé = False
            for c in range(nb_colonnes):
                if plan_jeu[0][c] == 0: 
                    plan_jeu[0][c] = 1  
                    mur_cassé = True
                    break
            if not mur_cassé:
                return plan_jeu 
            continue 
        visitées = []
        parcours_profondeur(plan_jeu, depart_ligne, depart_colonne, visitées ,nb_lignes , nb_colonnes)
        jetons_accessibles = 0
        for ligne, colonne in visitées:
            if plan_jeu[ligne][colonne] in [1, 2]:
                jetons_accessibles += 1
        if jetons_accessibles == total_jetons:
            return plan_jeu 
        mur_cassé = False
        for ligne in range(nb_lignes):
            for colonne in range(nb_colonnes):
                if plan_jeu[ligne][colonne] in [1, 2] and (ligne, colonne) not in visitées:
                    deplacements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for deplacement_ligne, deplacement_colonne in deplacements:
                        nouveau_ligne, nouveau_colonne = ligne + deplacement_ligne, colonne + deplacement_colonne
                        if 0 <= nouveau_ligne < nb_lignes and 0 <= nouveau_colonne < nb_colonnes and plan_jeu[nouveau_ligne][nouveau_colonne] == 0:
                            if nouveau_ligne == 0 :
                                plan_jeu[nouveau_ligne][nouveau_colonne] = 1
                            else :
                                plan_jeu[nouveau_ligne][nouveau_colonne] = 2 
                            mur_cassé = True
                            break 
                    if mur_cassé:
                        break 
            if mur_cassé:
                break     

def nombres_couleurs(plan_jeu, dictionnaire_couleurs) :
    """Calcule le nombre d'occurrences de chaque couleur de jeton."""
    compteur_couleurs = {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0, 'purple': 0}
    for (ligne, colonne), couleur in dictionnaire_couleurs.items():
        if plan_jeu[ligne][colonne] in [1, 2]:
            compteur_couleurs[couleur] += 1
    return compteur_couleurs

def corriger_multiple_3(plan_jeu, dictionnaire_couleurs) :
    """
    Vérifie si le compte de chaque couleur est un multiple de 3.
    Ajoute des jetons (en cassant des murs adjacents à un jeton existant) si nécessaire.
    """
    compteur = nombres_couleurs(plan_jeu, dictionnaire_couleurs)
    nb_lignes = len(plan_jeu)
    nb_colonnes = len(plan_jeu[0])
    for couleur, nombre in compteur.items():
        reste = nombre % 3
        if reste != 0:
            nb_a_ajouter = 3 - reste
            murs_adjacents_jeton = []
            for ligne in range(nb_lignes):
                for colonne in range(nb_colonnes):
                    if plan_jeu[ligne][colonne] == 0:
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        est_adjacent_a_jeton = False
                        for d_l, d_c in directions:
                            v_l, v_c = ligne + d_l, colonne + d_c
                            if 0 <= v_l < nb_lignes and 0 <= v_c < nb_colonnes and plan_jeu[v_l][v_c] in [1, 2]:
                                est_adjacent_a_jeton = True
                                break
                        if est_adjacent_a_jeton:
                            murs_adjacents_jeton.append((ligne, colonne))
            for i in range(min(nb_a_ajouter, len(murs_adjacents_jeton))):
                ligne, colonne = murs_adjacents_jeton.pop(0)
                if ligne == 0:
                    plan_jeu[ligne][colonne] = 1 # Type 1 si ligne 0
                else:
                    plan_jeu[ligne][colonne] = 2 # Type 2 pour le reste
                dictionnaire_couleurs[(ligne, colonne)] = couleur
    return plan_jeu, dictionnaire_couleurs

def initialiser_partie(difficulte="Moyen"): # Paramètre ajouté
    plan_jeu = generer_plan_plateau()
    plan_jeu = corriger_isolations(plan_jeu)
    
    # Gestion des couleurs selon la difficulté
    if difficulte == "Facile":
        couleurs_possibles = ['red', 'blue', 'green']
    elif difficulte == "Difficile":
        couleurs_possibles = ['red', 'blue', 'green', 'yellow', 'purple']
    else: # Moyen par défaut
        couleurs_possibles = ['red', 'blue', 'green', 'yellow']
        
    dictionnaire_couleurs = {}
    for indice_ligne in range(len(plan_jeu)):
        for indice_colonne in range(len(plan_jeu[0])):
            if plan_jeu[indice_ligne][indice_colonne] in [1, 2]:
                dictionnaire_couleurs[(indice_ligne, indice_colonne)] = random.choice(couleurs_possibles)
    plan_jeu, dictionnaire_couleurs = corriger_multiple_3(plan_jeu, dictionnaire_couleurs)    
    etat_ratelier = [None] * 5
    return plan_jeu, dictionnaire_couleurs, etat_ratelier

def verifier_victoire(plan_jeu):
    for ligne in plan_jeu:
        for case in ligne:
            if case in [1, 2]:
                return False
    return True

def liberation_voisins(plan_jeu, dictionnaire_couleurs, ligne_clic, colonne_clic, mode_daltonien=False):
    """Transforme les petits jetons (2) en gros (1) autour de la case cliquée (mise à jour pour le mode daltonien)"""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta_ligne, delta_colonne in directions:
        nouvelle_ligne, nouvelle_colonne = ligne_clic + delta_ligne, colonne_clic + delta_colonne
        if 0 <= nouvelle_ligne < len(plan_jeu) and 0 <= nouvelle_colonne < len(plan_jeu[0]):
            if plan_jeu[nouvelle_ligne][nouvelle_colonne] == 2:
                plan_jeu[nouvelle_ligne][nouvelle_colonne] = 1
                couleur = dictionnaire_couleurs.get((nouvelle_ligne, nouvelle_colonne), 'red')
                dessiner_case(nouvelle_ligne, nouvelle_colonne, 1, couleur, mode_daltonien) 

def gerer_ratelier(etat_ratelier, couleur_ajout, mode_daltonien=False):
    """
    Ajoute un jeton au râtelier et gère les suppressions par triplette.
    Retourne: (succes_ajout, a_perdu, points_bonus)
    """
    index_vide = -1
    for index in range(5):
        if etat_ratelier[index] is None:
            index_vide = index
            break 
    if index_vide == -1:
        temp_ratelier = list(etat_ratelier)
        temp_ratelier_index = 0
        while temp_ratelier[temp_ratelier_index] is not None:
             temp_ratelier_index = (temp_ratelier_index + 1) % 5
        temp_ratelier[temp_ratelier_index] = couleur_ajout
        compteur_couleurs = {}
        for couleur_jeton in temp_ratelier:
            if couleur_jeton is not None: 
                compteur_couleurs[couleur_jeton] = compteur_couleurs.get(couleur_jeton, 0) + 1
        nettoyage_effectue = False
        couleur_nettoyee = None
        for couleur_a_verifier, nombre_occurrences in compteur_couleurs.items():
            if nombre_occurrences >= 3:
                couleur_nettoyee = couleur_a_verifier
                nettoyage_effectue = True
                break     
        if nettoyage_effectue:
            for index in range(5):
                if etat_ratelier[index] == couleur_nettoyee:
                    etat_ratelier[index] = None
            index_vide = etat_ratelier.index(None) 
            etat_ratelier[index_vide] = couleur_ajout
            dessiner_ratelier(etat_ratelier, mode_daltonien)
            return True, False, 1
        else:
            return False, True, 0
    etat_ratelier[index_vide] = couleur_ajout
    dessiner_ratelier(etat_ratelier, mode_daltonien)
    compteur_couleurs = {}
    for couleur_jeton in etat_ratelier:
        if couleur_jeton is not None: 
            compteur_couleurs[couleur_jeton] = compteur_couleurs.get(couleur_jeton, 0) + 1
    points_gagnes = 0
    nettoyage_effectue = False
    for couleur_a_verifier, nombre_occurrences in compteur_couleurs.items():
        if nombre_occurrences >= 3:
            for index in range(5):
                if etat_ratelier[index] == couleur_a_verifier:
                    etat_ratelier[index] = None
            points_gagnes = 1
            nettoyage_effectue = True
            break
    if nettoyage_effectue:
        dessiner_ratelier(etat_ratelier, mode_daltonien)
        return True, False, points_gagnes
    if None not in etat_ratelier:
        return True, True, 0
    return True, False, 0

# --- ÉCRANS ET ANIMATIONS ---

def ecran_fin(message, sous_message, theme_couleur):
    efface_tout()
    if theme_couleur == 'CUSTOM':
        fond_final = '#000080'
    else:
        fond_final = theme_couleur
    rectangle(0, 0, 1200, 750, remplissage=fond_final, couleur=fond_final)
    texte(600, 300, message, taille=60, ancrage="center", couleur='gold')
    texte(600, 400, sous_message, taille=30, ancrage="center", couleur='white')
    texte(600, 600, "Cliquez pour quitter", taille=15, ancrage="center")
    mise_a_jour()
    attend_clic_gauche()

# --- MODES DE JEU ---

def mode_solo(theme_couleur, mode_daltonien_actif, difficulte): # Paramètre difficulte
    plan_jeu, dictionnaire_couleurs, etat_ratelier = initialiser_partie(difficulte)
    if theme_couleur == 'CUSTOM':
        dessiner_fond_personnalise('SOLO')
    else:
        rectangle(0, 0, 1200, 750, remplissage=theme_couleur, couleur=theme_couleur)
    rafraichir_plateau_entier(plan_jeu, dictionnaire_couleurs, mode_daltonien_actif)
    dessiner_ratelier(etat_ratelier, mode_daltonien_actif)
    rectangle(10, 10, 90, 40, couleur='black', remplissage='red')
    texte(50, 25, "MENU", ancrage='center', couleur='white')
    score_joueur = 0
    rectangle(828, 480, 970, 530, remplissage='white', couleur='black')
    texte(850, 500, "Score: 0", taille=20, tag="score")
    jeu_en_cours = True
    while jeu_en_cours:
        evenement = donne_ev()
        type_evenement = type_ev(evenement)
        if type_evenement == 'Quitte':
            jeu_en_cours = False  
        elif type_evenement == "ClicGauche":
            x_clic, y_clic = abscisse(evenement), ordonnee(evenement)
            if 10 < x_clic < 90 and 10 < y_clic < 40:
                ferme_fenetre()
                return
            ligne_clic, colonne_clic = pixels_vers_indices(x_clic, y_clic)
            if ligne_clic is not None and plan_jeu[ligne_clic][colonne_clic] == 1:
                couleur_jeton_capture = dictionnaire_couleurs[(ligne_clic, colonne_clic)]
                plan_jeu[ligne_clic][colonne_clic] = 4
                del dictionnaire_couleurs[(ligne_clic, colonne_clic)]
                dessiner_case(ligne_clic, colonne_clic, 4, mode_daltonien=mode_daltonien_actif)
                liberation_voisins(plan_jeu, dictionnaire_couleurs, ligne_clic, colonne_clic, mode_daltonien_actif)
                succes_ajout, perdu, points_gagners = gerer_ratelier(etat_ratelier, couleur_jeton_capture, mode_daltonien_actif)
                if points_gagners > 0:
                    point_bonus  = 1 if etat_ratelier.count(None) == 3 else 0
                    score_joueur += 1 + point_bonus
                    efface("score")
                    texte(850, 500, "Score: " + str(score_joueur), taille=20, tag="score")
                if perdu:
                    ecran_fin("GAME OVER", "Le râtelier est plein !", theme_couleur)
                    jeu_en_cours = False
                elif verifier_victoire(plan_jeu):
                    ecran_fin("VICTOIRE !", "Plateau nettoyé !", theme_couleur)
                    jeu_en_cours = False
                    return score_joueur
        mise_a_jour()

def mode_VS(theme_couleur, mode_daltonien_actif, difficulte): # Paramètre difficulte
    plan_jeu, dictionnaire_couleurs, etat_ratelier = initialiser_partie(difficulte)
    if theme_couleur == 'CUSTOM':
        dessiner_fond_personnalise('VS')
    else:
        rectangle(0, 0, 1200, 750, remplissage=theme_couleur, couleur=theme_couleur)
    rafraichir_plateau_entier(plan_jeu, dictionnaire_couleurs, mode_daltonien_actif)
    dessiner_ratelier(etat_ratelier, mode_daltonien_actif)
    rectangle(10, 10, 90, 40, couleur='black', remplissage='red')
    texte(50, 25, "MENU", ancrage='center', couleur='white')
    joueur_actuel = 1
    scores_joueurs = {1: 0, 2: 0}
    def mettre_a_jour_affichage_scores():
        efface("info_vs")
        if joueur_actuel == 1:
            couleur_texte_j1 = 'green'
        else:
            couleur_texte_j1 = 'black'
        rectangle(810, 480, 1100, 620, remplissage='white', couleur='black', tag="info_vs")
        texte(850, 500, "Joueur 1: " + str(scores_joueurs[1]), couleur=couleur_texte_j1, tag="info_vs")
        if joueur_actuel == 2:
            couleur_texte_j2 = 'green'
        else:
            couleur_texte_j2 = 'black'
        texte(850, 530, "Joueur 2: " + str(scores_joueurs[2]), couleur=couleur_texte_j2, tag="info_vs")
        texte(850, 580, "Tour: Joueur " + str(joueur_actuel), couleur='blue', tag="info_vs")
    mettre_a_jour_affichage_scores()
    jeu_en_cours = True
    while jeu_en_cours:
        evenement = donne_ev()
        type_evenement = type_ev(evenement)
        if type_evenement == 'Quitte':
            jeu_en_cours = False
        elif type_evenement == "ClicGauche":
            x_clic, y_clic = abscisse(evenement), ordonnee(evenement)
            if 10 < x_clic < 90 and 10 < y_clic < 40:
                ferme_fenetre()
                return
            ligne_clic, colonne_clic = pixels_vers_indices(x_clic, y_clic)
            if ligne_clic is not None and plan_jeu[ligne_clic][colonne_clic] == 1:
                couleur_jeton_capture = dictionnaire_couleurs[(ligne_clic, colonne_clic)]
                plan_jeu[ligne_clic][colonne_clic] = 4
                del dictionnaire_couleurs[(ligne_clic, colonne_clic)]
                dessiner_case(ligne_clic, colonne_clic, 4, mode_daltonien=mode_daltonien_actif)
                liberation_voisins(plan_jeu, dictionnaire_couleurs, ligne_clic, colonne_clic, mode_daltonien_actif)
                succes_ajout, perdu, points_gagners = gerer_ratelier(etat_ratelier, couleur_jeton_capture, mode_daltonien_actif)
                if points_gagners > 0:
                        point_bonus  = 1 if etat_ratelier.count(None) == 3 else 0
                        scores_joueurs[joueur_actuel] += 1 + point_bonus
                        print("Joueur " + str(joueur_actuel) + " fait une triplette !")
                else:
                    joueur_actuel = 3 - joueur_actuel
                mettre_a_jour_affichage_scores()
                if perdu:
                    gagnant = 3 - joueur_actuel 
                    ecran_fin("Joueur " + str(gagnant) + " Gagne !", "L'adversaire a bloqué le râtelier", theme_couleur)
                    jeu_en_cours = False
                elif verifier_victoire(plan_jeu):
                    if scores_joueurs[1] > scores_joueurs[2]:
                        gagnant = 1
                    elif scores_joueurs[2] > scores_joueurs[1]:
                        gagnant = 2
                    else:
                        gagnant = "Égalité"
                    ecran_fin("FIN DE PARTIE", "Vainqueur : " + str(gagnant), theme_couleur)
                    jeu_en_cours = False
        mise_a_jour()

# --- MENU PRINCIPAL ---

def menu_principal():
    cree_fenetre(1200, 750)
    couleurs_themes = ['#FFFFFF', '#10E311', '#ED8E00', '#CF0000', '#73DFFF', 'CUSTOM']
    noms_themes = ['Blanc', 'Vert', 'Orange', 'Rouge', 'Bleu', 'Personnalisé']
    index_couleur_theme = 0
    mode_jeu_selectionne = 'SOLO'
    mode_daltonien_actif = False
    
    # Paramètres Difficulté
    difficultes = ["Facile", "Moyen", "Difficile"]
    index_difficulte = 1 # Moyen par défaut
    
    en_menu = True
    while en_menu:
        efface_tout()
        theme_actuel = couleurs_themes[index_couleur_theme]
        if theme_actuel == 'CUSTOM':
            rectangle(0, 0, 1200, 750, remplissage='grey', couleur='grey')
        else:
            rectangle(0, 0, 1200, 750, remplissage=theme_actuel, couleur=theme_actuel)
        
        rectangle(500, 100, 700, 200, couleur='black', remplissage='white')
        texte(600, 150, 'PickTok', taille=28, ancrage='center')
        
        rectangle(500, 520, 700, 580, couleur='black', remplissage='#10E311')
        texte(600, 550, 'JOUER', taille=22, ancrage='center')
        
        # Sélecteur Thème
        texte(600, 230, "Couleur: " + str(noms_themes[index_couleur_theme]), ancrage='center')
        texte(450, 230, "<", taille=20, couleur='blue')
        texte(750, 230, ">", taille=20, couleur='blue')
        
        # Sélecteur Difficulté
        texte(600, 280, "Difficulté: " + str(difficultes[index_difficulte]), ancrage='center')
        texte(450, 280, "<", taille=20, couleur='blue')
        texte(750, 280, ">", taille=20, couleur='blue')
        
        # Sélecteur Mode
        if mode_jeu_selectionne == 'SOLO':
            couleur_solo = 'red'
            couleur_vs = 'black'
        elif mode_jeu_selectionne == 'VS':
            couleur_solo = 'black'
            couleur_vs = 'red'
        texte(550, 340, "SOLO", couleur=couleur_solo, ancrage='center')
        texte(650, 340, "VS", couleur=couleur_vs, ancrage='center')
        
        # Daltonien
        texte(600, 400, "Mode Accès (Formes) :", ancrage='center')
        couleur_etat = 'green' if mode_daltonien_actif else 'black'
        texte(600, 445, "ACTIVÉ" if mode_daltonien_actif else "DÉSACTIVÉ", 
              couleur=couleur_etat, ancrage='center', tag='acces_etat')
        rectangle(480, 420, 720, 460, couleur='grey', epaisseur=1)
        
        mise_a_jour()
        evenement = attend_ev()
        type_evenement = type_ev(evenement)
        if type_evenement == 'Quitte':
            ferme_fenetre()
            return None, None, None, None # Retourne 4 valeurs maintenant
        elif type_evenement == 'ClicGauche':
            x_clic, y_clic = abscisse(evenement), ordonnee(evenement)
            
            # Jouer
            if 500 < x_clic < 700 and 520 < y_clic < 580:
                efface_tout()
                return theme_actuel, mode_jeu_selectionne, mode_daltonien_actif, difficultes[index_difficulte]
            
            # Thème
            if 210 < y_clic < 250:
                if 430 < x_clic < 470:
                    index_couleur_theme = (index_couleur_theme - 1) % len(couleurs_themes)
                elif 730 < x_clic < 770:
                    index_couleur_theme = (index_couleur_theme + 1) % len(couleurs_themes)
            
            # Difficulté
            if 260 < y_clic < 300:
                if 430 < x_clic < 470:
                    index_difficulte = (index_difficulte - 1) % len(difficultes)
                elif 730 < x_clic < 770:
                    index_difficulte = (index_difficulte + 1) % len(difficultes)
                    
            # Mode
            if 320 < y_clic < 360:
                if 500 < x_clic < 600:
                    mode_jeu_selectionne = 'SOLO'
                elif 600 < x_clic < 700:
                    mode_jeu_selectionne = 'VS'
            
            # Daltonien
            if 480 < x_clic < 720 and 420 < y_clic < 460:
                mode_daltonien_actif = not mode_daltonien_actif

# --- PROGRAMME PRINCIPAL ---
pseudo = input("Quel est votre nom ?")
while True:
    res = menu_principal()
    if res[0] is None:
        break
    theme_choisi, mode_choisi, acces_actif, diff_choisie = res
    if mode_choisi == 'SOLO':
        score_joueur = mode_solo(theme_choisi, acces_actif, diff_choisie)
        if type(score_joueur) == int :
            main_leaderboard(score_joueur , pseudo)
    elif mode_choisi == 'VS':
        mode_VS(theme_choisi, acces_actif, diff_choisie)