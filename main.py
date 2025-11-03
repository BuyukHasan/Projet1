from fltk import*
from random import randint


def creer_plateau_avec_couleurs(plan_plateau):
    """
    Crée un plateau avec des couleurs fixes pour chaque jeton
    
    Args:
        plan_plateau (list): Matrice 2D représentant le plateau de jeu
        
    Returns:
        tuple: (plan_plateau, dict_couleurs) où dict_couleurs associe chaque position (ligne, colonne) 
               à une couleur fixe pour les jetons
    """
    # Liste des couleurs possibles pour les jetons
    liste_couleurs = ['red', 'blue', 'green', 'yellow']
    dict_couleurs = {} # Dictionnaire qui va enregistrer la couleur du jeton à la ligne et colonne correspondante
    
    # Parcours de toutes les cases du plateau
    for ligne in range(len(plan_plateau)): # On parcours ligne par ligne 
        for colonne in range(len(plan_plateau[0])): # On parcours colonne par colonne 
            if plan_plateau[ligne][colonne] in [1, 2]: # Si on trouve un jeton (1=gros, 2=petit)
                # Attribution d'une couleur aléatoire mais fixe pour ce jeton
                dict_couleurs[(ligne, colonne)] = liste_couleurs[randint(0, 3)] 
    
    return plan_plateau, dict_couleurs # On retourne le plan du plateau ainsi que la couleur de chaque jeton


def dessiner_jeton(x1, y1, x2, y2, type_jeton, couleur_jeton):
    """
    Dessine un jeton dans une case donnée avec une couleur spécifique
    
    Args:
        x1, y1 (int): Coin supérieur gauche de la case
        x2, y2 (int): Coin inférieur droit de la case
        type_jeton (int): 1 = gros jeton (capturable), 2 = petit jeton (non capturable)
        couleur_jeton (str): Couleur fixe du jeton
    """
    # Calcul du centre de la case
    centre_x = (x1 + x2) / 2 # Coordonnées en x du cercle
    centre_y = (y1 + y2) / 2 # Coordonnées en y du cercle
    
    if type_jeton == 1: # Si c'est 1 alors on dessine un jeton capturable (plein)
        cercle(centre_x, centre_y, 20, couleur='black', remplissage=couleur_jeton)
    else:  # Sinon c'est un jeton non capturable (creux avec petit cercle intérieur)
        cercle(centre_x, centre_y, 20, couleur='black') # Cercle extérieur vide
        cercle(centre_x, centre_y, 10, couleur='black', remplissage=couleur_jeton) # Cercle intérieur plein


def dessiner_jeton_supplementaire(x1, y1, x2, y2, couleur_jeton):
    """
    Dessine un jeton dans une case supplémentaire (toujours un gros jeton)
    
    Args:
        x1, y1 (int): Coin supérieur gauche de la case
        x2, y2 (int): Coin inférieur droit de la case  
        couleur_jeton (str): Couleur du jeton à dessiner
    """
    centre_x = (x1 + x2) / 2 
    centre_y = (y1 + y2) / 2
    # Dessine un jeton capturable (plein)
    cercle(centre_x, centre_y, 20, couleur='black', remplissage=couleur_jeton)


def liberation_jeton(plan_plateau, dict_couleurs, ligne_centre, colonne_centre):
    """
    Transforme les petits jetons adjacents en gros jetons en conservant leurs couleurs
    lorsqu'un jeton est capturé au centre
    
    Args:
        plan_plateau (list): Matrice du plateau de jeu
        dict_couleurs (dict): Dictionnaire des couleurs des jetons
        ligne_centre (int): Ligne du jeton capturé
        colonne_centre (int): Colonne du jeton capturé
        
    Returns:
        int: Nombre de jetons libérés (transformés)
    """
    hauteur = len(plan_plateau) # Nombre de lignes
    largeur = len(plan_plateau[0]) # Nombre de colonnes
    
    # Directions des cases adjacentes (haut, bas, gauche, droite)
    directions = [
        (-1, 0),  # haut car on recule d'une ligne
        (1, 0),   # bas car on avance d'une ligne 
        (0, -1),  # gauche car on recule d'une colonne
        (0, 1)    # droite car on avance d'une colonne
    ]
    
    cases_liberees = 0 # Le nombre de cases adjacentes traitées
    
    # Vérification des 4 cases adjacentes
    for dl, dc in directions: # On regarde les cases adjacentes du jeton retiré
        nouvelle_ligne = ligne_centre + dl 
        nouvelle_colonne = colonne_centre + dc
        
        # Vérification que la case adjacente est dans les limites du plateau
        if 0 <= nouvelle_ligne < hauteur and 0 <= nouvelle_colonne < largeur:
            if plan_plateau[nouvelle_ligne][nouvelle_colonne] == 2: # Si c'est un jeton non capturable
                plan_plateau[nouvelle_ligne][nouvelle_colonne] = 1 # Transformation en jeton capturable
                cases_liberees += 1 
                print("Jeton libéré à la position" +  str((nouvelle_ligne, nouvelle_colonne)))
                
                # Récupération de la couleur existante du jeton
                couleur_existante = dict_couleurs.get((nouvelle_ligne, nouvelle_colonne), 'red')
                
                # Calcul des coordonnées de la case à redessiner
                x1 = 100 + nouvelle_colonne * 50
                y1 = 100 + nouvelle_ligne * 50
                x2 = x1 + 50
                y2 = y1 + 50
                
                # Effacement et redessin du jeton avec son nouveau type
                rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
                dessiner_jeton(x1, y1, x2, y2, 1, couleur_existante)
    
    # Affichage des résultats de la libération
    if cases_liberees > 0:
        print(str(cases_liberees) + " jeton(s) libéré(s) autour de la position " + str((ligne_centre, colonne_centre)))
    else:
        print("Aucun jeton à libérer autour de la position" + str((ligne_centre, colonne_centre)))
    
    return cases_liberees


def redessiner_cases_supplementaires(etat_cases_supplementaires):
    """
    Redessine toutes les cases supplémentaires selon leur état actuel
    
    Args:
        etat_cases_supplementaires (list): Liste des couleurs des jetons dans les cases supplémentaires
    """
    # Les coordonnées fixes des 5 cases supplémentaires
    cases_coords = [
        (550, 100, 600, 150),   # Case 1
        (550, 150, 600, 200),   # Case 2  
        (550, 200, 600, 250),   # Case 3
        (550, 250, 600, 300),   # Case 4
        (550, 300, 600, 350)    # Case 5
    ]
    
    # Redessine toutes les cases
    for i in range(len(etat_cases_supplementaires)):
        x1, y1, x2, y2 = cases_coords[i]
        
        # Efface la case
        rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
        
        # Redessine le jeton si présent
        if etat_cases_supplementaires[i] is not None:
            dessiner_jeton_supplementaire(x1, y1, x2, y2, etat_cases_supplementaires[i])


def verification_case_supplémentaire(etat_cases_supplementaires):
    """
    Vérifie les cases supplémentaires et supprime les groupes de 3 jetons de même couleur
    Vérifie également si toutes les cases sont remplies (condition de défaite)
    
    Args:
        etat_cases_supplementaires (list): Liste des couleurs dans les cases supplémentaires
        
    Returns:
        tuple: ("défaite" ou nombre_jetons_supprimés, nombre_groupes_supprimés)
    """
    # Compte le nombre de jetons de chaque couleur
    compteur_couleurs = {}
    for couleur in etat_cases_supplementaires:
        if couleur is not None:
            compteur_couleurs[couleur] = compteur_couleurs.get(couleur, 0) + 1
    
    # Vérifie s'il y a une couleur avec au moins 3 jetons
    jetons_supprimes = 0
    groupes_supprimes = 0
    for couleur, count in compteur_couleurs.items():
        if count >= 3:
            # Supprime TOUS les jetons de cette couleur
            for i in range(len(etat_cases_supplementaires)):
                if etat_cases_supplementaires[i] == couleur:
                    etat_cases_supplementaires[i] = None
                    jetons_supprimes += 1
            
            groupes_supprimes += 1
            print(str(jetons_supprimes) + "jetons" + str(couleur) + "supprimés des cases supplémentaires")
            
            # Redessine les cases supplémentaires après suppression
            redessiner_cases_supplementaires(etat_cases_supplementaires)
            break  # On supprime seulement une couleur à la fois
    
    # Vérification si toutes les cases sont remplies (défaite) - APRÈS les suppressions
    if all(case is not None for case in etat_cases_supplementaires):
        return "défaite", groupes_supprimes
    
    return jetons_supprimes, groupes_supprimes


def ajouter_jeton_supplementaire(etat_cases_supplementaires, couleur_jeton, compteur_groupes):
    """
    Ajoute un jeton à la première case supplémentaire disponible
    Vérifie les conditions de groupe et de défaite après l'ajout
    
    Args:
        etat_cases_supplementaires (list): État actuel des cases supplémentaires
        couleur_jeton (str): Couleur du jeton à ajouter
        compteur_groupes (int): Compteur actuel des groupes supprimés
        
    Returns:
        tuple: (défaite, nouveau_compteur) où défaite est un booléen indiquant si le jeu est perdu
    """
    # Les coordonnées fixes des cases supplémentaires
    cases_coords = [
        (550, 100, 600, 150),   # Case 1
        (550, 150, 600, 200),   # Case 2  
        (550, 200, 600, 250),   # Case 3
        (550, 250, 600, 300),   # Case 4
        (550, 300, 600, 350)    # Case 5
    ]
    
    # Trouve la première case vide
    for i in range(len(etat_cases_supplementaires)):
        if etat_cases_supplementaires[i] is None:
            # Ajoute le jeton dans la case vide
            etat_cases_supplementaires[i] = couleur_jeton
            x1, y1, x2, y2 = cases_coords[i]
            dessiner_jeton_supplementaire(x1, y1, x2, y2, couleur_jeton)
            print("Jeton"+ str(couleur_jeton)+ "ajouté à la case supplémentaire"+ str(i+1))
            
            # Vérifie les conditions après ajout (suppression des groupes de 3 d'abord)
            resultat_verification, nouveaux_groupes = verification_case_supplémentaire(etat_cases_supplementaires)
            
            # Met à jour le compteur de groupes
            compteur_groupes += nouveaux_groupes
            
            if resultat_verification == "défaite":
                print("Après suppression des groupes, toutes les cases sont encore remplies - DÉFAITE !")
                return True, compteur_groupes  # Retourne True pour indiquer la défaite
            elif resultat_verification > 0:
                print(str(resultat_verification) + "jetons supprimés des cases supplémentaires")
                print("Groupes supprimés: " + str(nouveaux_groupes) + "- Total: " + str(compteur_groupes))
            
            return False, compteur_groupes  # Retourne False pour continuer le jeu
    
    print("Erreur : Aucune case vide trouvée alors qu'on devrait en avoir")
    return False, compteur_groupes


def prendre_jeton(plan_plateau, dict_couleurs, etat_cases_supplementaires, x_clic, y_clic, compteur_groupes):
    """
    Gère la capture d'un jeton : fait disparaître un gros jeton et l'ajoute aux cases supplémentaires
    
    Args:
        plan_plateau (list): Matrice du plateau de jeu
        dict_couleurs (dict): Dictionnaire des couleurs des jetons
        etat_cases_supplementaires (list): État des cases supplémentaires
        x_clic, y_clic (int): Coordonnées du clic de souris
        compteur_groupes (int): Compteur actuel des groupes supprimés
        
    Returns:
        tuple: (résultat, nouveau_compteur) où résultat peut être "défaite", True (succès) ou False (échec)
    """
    # Vérification que le clic est dans la zone du plateau principal
    if not (100 <= x_clic <= 500 and 100 <= y_clic <= 600):
        return False, compteur_groupes
    
    # Conversion des coordonnées écran en indices de matrice
    colonne = (x_clic - 100) // 50
    ligne = (y_clic - 100) // 50
    
    # Vérification que les indices sont valides
    if 0 <= ligne < len(plan_plateau) and 0 <= colonne < len(plan_plateau[0]):
        if plan_plateau[ligne][colonne] == 1:  # Si c'est un gros jeton capturable
            # Récupère la couleur du jeton avant de le supprimer
            couleur_jeton = dict_couleurs.get((ligne, colonne), 'red')
            
            # Marque la case comme vide
            plan_plateau[ligne][colonne] = 4
            print("Jeton pris à la position" + str((ligne, colonne)))
            
            # Calcul des coordonnées pour redessiner
            x1 = 100 + colonne * 50
            y1 = 100 + ligne * 50
            x2 = x1 + 50
            y2 = y1 + 50
            
            # Efface le jeton
            rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
            
            # Ajoute le jeton aux cases supplémentaires
            défaite, nouveau_compteur = ajouter_jeton_supplementaire(etat_cases_supplementaires, couleur_jeton, compteur_groupes)
            
            # Si défaite est True, on arrête tout
            if défaite:
                return "défaite", nouveau_compteur
            
            # Supprime la couleur du jeton pris du dictionnaire
            if (ligne, colonne) in dict_couleurs:
                del dict_couleurs[(ligne, colonne)]
            
            # Libère les jetons adjacents
            liberation_jeton(plan_plateau, dict_couleurs, ligne, colonne)
            
            return True, nouveau_compteur
        else:
            print("Case " + str((ligne, colonne)) + "- Pas un gros jeton (valeur: "+ str(plan_plateau[ligne][colonne]))
            return False, compteur_groupes
    else:
        return False, compteur_groupes


def afficher_animation_défaite():
    """
    Affiche l'écran de défaite avec animation et message
    Attend un clic ou la fermeture de la fenêtre pour terminer
    """
    # Efface tout l'écran
    efface_tout()
    
    # Redessine le fond avec le thème
    rectangle(0, 0, 1200, 750, remplissage=theme, couleur=theme)
    
    # Affiche le gif de défaite
    try:
        # Centre le gif dans la fenêtre
        image(600, 400, "../../../Desktop/hq720.jpg", ancrage="center")
        print("Animation de défaite affichée !")
        texte(600, 125, "GameOver", taille=100, ancrage="center", couleur='red')
    except:
        print("Fichier gif non trouvé - affichage du message de défaite")
    
    # Met à jour l'affichage
    mise_a_jour()
    
    # Attend que l'utilisateur clique ou ferme la fenêtre
    while True:
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == 'Quitte' or tev == 'ClicGauche':
            break


def afficher_animation_victoire(compteur_groupes):
    """
    Affiche l'écran de victoire avec animation et statistiques
    
    Args:
        compteur_groupes (int): Nombre total de groupes supprimés pendant la partie
    """
    # Efface tout l'écran
    efface_tout()
    
    # Redessine le fond avec le thème
    rectangle(0, 0, 1200, 750, remplissage=theme, couleur=theme)
    
    # Affiche l'animation de victoire
    try:
        # Centre l'image dans la fenêtre
        image(600, 400, "../../../Desktop/xf870.jpg", ancrage="center")
        print("Animation de victoire affichée !")
        texte(600, 125, "Victoire !", taille=100, ancrage="center", couleur='green')
        texte(600, 200, "Félicitations !", taille=50, ancrage="center", couleur='gold')
        texte(600, 280, "Groupes supprimés: " + str(compteur_groupes), taille=30, ancrage="center", couleur='white')
    except:
        print("Fichier image non trouvé - affichage du message de victoire")
        texte(600, 300, "VICTOIRE !", taille=80, ancrage="center", couleur='green')
        texte(600, 400, "Vous avez nettoyé tout le plateau !", taille=30, ancrage="center", couleur='white')
        #texte(600, 450, f"Groupes supprimés: {compteur_groupes}", taille=25, ancrage="center", couleur='white')
    
    # Met à jour l'affichage
    mise_a_jour()
    
    # Attend que l'utilisateur clique ou ferme la fenêtre
    while True:
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == 'Quitte' or tev == 'ClicGauche':
            break


def verifier_victoire(plan_plateau):
    """
    Vérifie s'il n'y a plus aucun jeton sur le plateau (condition de victoire)
    
    Args:
        plan_plateau (list): Matrice du plateau de jeu
        
    Returns:
        bool: True si victoire (plus de jetons), False sinon
    """
    for ligne in range(len(plan_plateau)):
        for colonne in range(len(plan_plateau[0])):
            if plan_plateau[ligne][colonne] in [1, 2]:  # S'il reste des gros ou petits jetons
                return False
    return True


def vider_cases_supplementaires(etat_cases_supplementaires):
    """
    Vide toutes les cases supplémentaires et les redessine vides
    
    Args:
        etat_cases_supplementaires (list): Liste des cases supplémentaires à vider
    """
    # Réinitialise l'état des cases
    for i in range(len(etat_cases_supplementaires)):
        etat_cases_supplementaires[i] = None
    
    # Redessine les cases vides
    x1 = 550
    y1 = 100
    x2 = 600
    y2 = 150
    
    for grille in range(5):
        rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
        y1 += 50
        y2 += 50
    
    print("Cases supplémentaires vidées")


def initialiser_cases_supplementaires():
    """
    Initialise les cases supplémentaires (vides au début du jeu)
    
    Returns:
        list: Liste de 5 éléments None représentant les cases vides
    """
    # Dessine les cases vides
    x1 = 550
    y1 = 100
    x2 = 600
    y2 = 150
    
    for grille in range(5):
        rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
        y1 += 50
        y2 += 50
    
    # Retourne une liste de 5 éléments None (cases vides)
    return [None] * 5


def mettre_a_jour_score(compteur_groupes):
    """
    Met à jour l'affichage du score (nombre de groupes supprimés)
    
    Args:
        compteur_groupes (int): Nouveau nombre de groupes supprimés
    """
    # Efface la zone du score
    rectangle(750, 500, 950, 600, remplissage='white', couleur='black')
    
    # Affiche le nouveau score
    texte(850, 525, "Score:", taille=15, ancrage="center")
    texte(850, 550, str(compteur_groupes) + "groupes", taille=15, ancrage="center")


def parametre_fenetre():
    """
    Configure la fenêtre graphique avec les paramètres de base
    
    Returns:
        str: La couleur du thème choisi par l'utilisateur
    """
    # Demande la couleur de thème à l'utilisateur
    theme = input('Quelle couleur? ')
    
    # Crée la fenêtre
    cree_fenetre(1200,750)
    
    # Dessine le fond
    rectangle(0,0,1200,1200, remplissage=theme, couleur=theme)
    
    # Dessine le titre du jeu
    rectangle(650,100,1050,200, couleur='black', remplissage='white')
    texte(850, 150, "Pick Tok", taille=30, ancrage="center")
    
    # Dessine la zone de score initiale
    rectangle(750,500,950,600, couleur='black', remplissage='white')
    texte(850, 525, "Score:", taille=15, ancrage="center")
    texte(850, 550, "0 groupes", taille=15, ancrage="center")
    
    return theme


def generer_plan_plateau():
    """
    Génère aléatoirement le plan initial du plateau de jeu
    
    Returns:
        list: Matrice 10x8 représentant le plateau initial avec :
              - 0 : mur (case noire)
              - 1 : gros jeton (capturable, seulement sur la première ligne)
              - 2 : petit jeton (non capturable)
    """
    plan_plateau = []
    
    # Génération de 10 lignes
    for ligne in range(10):
        ligne_plan = []
        # Génération de 8 colonnes
        for colonne in range(8):
            if randint(0, 3) == 3:  # 1 chance sur 4 d'avoir un mur
                ligne_plan.append(0)
            else:
                if ligne == 0:  # Première ligne : seulement des gros jetons
                    ligne_plan.append(1)
                else:  # Autres lignes : petits jetons
                    ligne_plan.append(2)
        plan_plateau.append(ligne_plan)
    
    return plan_plateau


def anti_isolation(plan_plateau, case_isolee):
    """
    Supprime une case isolée en transformant un mur adjacent en jeton
    
    Args:
        plan_plateau (list): Matrice du plateau de jeu
        case_isolee (tuple): (ligne, colonne) de la case isolée à corriger
        
    Returns:
        bool: True si une correction a été appliquée, False sinon
    """
    ligne, colonne = case_isolee
    hauteur = len(plan_plateau)
    largeur = len(plan_plateau[0])
    
    # Liste des directions possibles pour supprimer un mur
    directions = []
    
    # Vérification des 4 directions possibles
    if ligne > 0 and plan_plateau[ligne-1][colonne] == 0: #si y'a mur juste au dessus de la case sans dépasser le plateau
        directions.append(('haut', ligne-1, colonne))
    if ligne < hauteur-1 and plan_plateau[ligne+1][colonne] == 0: #si y'a mur juste en dessous de la case sans dépasser le plateau
        directions.append(('bas', ligne+1, colonne))
    if colonne > 0 and plan_plateau[ligne][colonne-1] == 0: #si y'a mur juste à gauche de la case sans dépasser le plateau
        directions.append(('gauche', ligne, colonne-1))
    if colonne < largeur-1 and plan_plateau[ligne][colonne+1] == 0: #si y'a mur juste à droite de la case sans dépasser le plateau
        directions.append(('droite', ligne, colonne+1))
    
    # Si au moins une direction est disponible
    if directions:
        # Choix aléatoire d'une direction
        direction_choisie, ligne_mur, colonne_mur = directions[randint(0, len(directions)-1)]
        
        # Transformation du mur en jeton
        if ligne_mur == 0: 
            plan_plateau[ligne_mur][colonne_mur] = 1  # Gros jeton sur la première ligne
        else:
            plan_plateau[ligne_mur][colonne_mur] = 2  # Petit jeton ailleurs
        
        print("Mur supprimé en position " + str((ligne_mur,colonne_mur)) + "- direction" + str(direction_choisie))
        
        return True
    else:
        print("Aucune direction disponible pour supprimer l'isolation")
        return False


def verification_plateau(plan_plateau):
    """
    Vérifie le plateau pour détecter les cases isolées (entièrement entourées de murs)
    et les corrige automatiquement
    
    Args:
        plan_plateau (list): Matrice du plateau à vérifier
        
    Returns:
        tuple: (détecté, plan_corrigé) où détecté est un booléen indiquant si des corrections ont été faites
    """
    detecter = False
    cases_isolees = []
    hauteur = len(plan_plateau)
    largeur = len(plan_plateau[0])
    
    # Parcours de toutes les cases du plateau
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if plan_plateau[ligne][colonne] in [1, 2]:  # Si c'est un jeton
                murs_autour = 0
                
                # Compte le nombre de murs autour de la case
                if ligne == 0 or plan_plateau[ligne-1][colonne] == 0:
                    murs_autour += 1
                if ligne == hauteur-1 or plan_plateau[ligne+1][colonne] == 0:
                    murs_autour += 1
                if colonne == 0 or plan_plateau[ligne][colonne-1] == 0:
                    murs_autour += 1
                if colonne == largeur-1 or plan_plateau[ligne][colonne+1] == 0:
                    murs_autour += 1
                
                # Si la case est entièrement entourée de murs (4 côtés)
                if murs_autour == 4:
                    detecter = True
                    cases_isolees.append((ligne, colonne))
                    print("Case isolée détectée à la position " + str((ligne, colonne)))
    
    # Correction des cases isolées détectées
    if detecter:
        print(str(len(cases_isolees)) + "case(s) isolée(s) détectée(s) - correction en cours...")
        for case in cases_isolees:
            anti_isolation(plan_plateau, case)
    else:
        print("Aucune case isolée détectée") 
    
    return detecter, plan_plateau


def generer_dessin_plateau(plan_plateau, dict_couleurs):
    """
    Génère le dessin graphique du plateau avec les couleurs fixes
    
    Args:
        plan_plateau (list): Matrice du plateau de jeu
        dict_couleurs (dict): Dictionnaire des couleurs des jetons
    """
    # Dessine le fond du plateau
    rectangle(95, 95, 505, 605, couleur='white', remplissage='white')
    
    # Coordonnées initiales de la première case
    x1 = 100
    y1 = 100
    x2 = 150
    y2 = 150
    
    # Parcours de toutes les cases pour les dessiner
    for ligne in range(len(plan_plateau)):
        for colonne in range(len(plan_plateau[0])):
            if plan_plateau[ligne][colonne] == 0:  # Mur
                rectangle(x1, y1, x2, y2, remplissage='black', couleur='black')
            elif plan_plateau[ligne][colonne] in [1, 2]:  # Jeton
                rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
                # Récupère la couleur fixe du jeton
                couleur_jeton = dict_couleurs.get((ligne, colonne), 'red')
                dessiner_jeton(x1, y1, x2, y2, plan_plateau[ligne][colonne], couleur_jeton)
            else:  # Case vide (4)
                rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
            
            # Passage à la colonne suivante
            x1 += 50
            x2 += 50
        
        # Retour à la première colonne, passage à la ligne suivante
        x1 = 100
        x2 = 150
        y1 += 50
        y2 += 50


# PROGRAMME PRINCIPAL
# ===================

# Initialisation de la fenêtre et du thème
theme = parametre_fenetre()

# Génération et validation du plateau
plan_initial = generer_plan_plateau()
print("Plan initial généré:")
for ligne in plan_initial:
    print(ligne)

# Vérification et correction des cases isolées
detecter, plan_valide = verification_plateau(plan_initial)

print("Plan après correction:")
for ligne in plan_valide:
    print(ligne)

# Création du plateau avec couleurs fixes
plan_valide, dict_couleurs = creer_plateau_avec_couleurs(plan_valide)

# Initialisation des cases supplémentaires
etat_cases_supplementaires = initialiser_cases_supplementaires()

# Dessin du plateau principal
generer_dessin_plateau(plan_valide, dict_couleurs)

# Initialisation du compteur de groupes et de l'état du jeu
compteur_groupes = 0
jeu_en_cours = True

# BOUCLE PRINCIPALE DU JEU
while jeu_en_cours:
    ev = donne_ev()
    tev = type_ev(ev)
    
    if tev == 'Quitte':  # Fermeture de la fenêtre
        break
    elif tev == "ClicGauche":  # Clic de souris
        x_clic = abscisse(ev)
        y_clic = ordonnee(ev)
        print("Clic gauche au point", (x_clic, y_clic))
        
        # Tentative de prise de jeton
        resultat, nouveau_compteur = prendre_jeton(plan_valide, dict_couleurs, etat_cases_supplementaires, x_clic, y_clic, compteur_groupes)
        
        # Met à jour le compteur
        compteur_groupes = nouveau_compteur
        
        # Met à jour l'affichage du score
        mettre_a_jour_score(compteur_groupes)
        
        # Vérification des conditions de fin de jeu
        if resultat == "défaite":  # Défaite : cases supplémentaires pleines
            afficher_animation_défaite()
            jeu_en_cours = False
        elif resultat:  # Si un jeton a été pris avec succès
            # Vérifie si le plateau est vide (victoire)
            if verifier_victoire(plan_valide):
                print("Victoire ! Le plateau est vide !")
                afficher_animation_victoire(compteur_groupes)
                jeu_en_cours = False
    
    mise_a_jour()

# FERMETURE DU JEU
if not jeu_en_cours:
    ferme_fenetre()
else:
    attend_fermeture()