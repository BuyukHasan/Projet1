from fltk import*
from random import randint


def dessiner_jeton(x1, y1, x2, y2, type_jeton, liste_couleurs):
    """
    Dessine un jeton dans une case donnée
    x1, y1: coin supérieur gauche de la case
    x2, y2: coin inférieur droit de la case
    type_jeton: 1 = gros jeton, 2 = petit jeton
    liste_couleurs: liste des couleurs disponibles
    """
    centre_x = (x1 + x2) / 2
    centre_y = (y1 + y2) / 2
    couleur_jeton = liste_couleurs[randint(0, 3)]
    
    if type_jeton == 1: 
        cercle(centre_x, centre_y, 20, couleur='black', remplissage=couleur_jeton)
    else: 
        cercle(centre_x, centre_y, 20, couleur='black')
        cercle(centre_x, centre_y, 10, couleur='black', remplissage=couleur_jeton)

def liberation_jeton(plan_plateau, ligne_centre, colonne_centre):
    """
    Transforme les petits jetons adjacents en gros jetons
    plan_plateau: le plan du plateau
    ligne_centre, colonne_centre: position du jeton pris
    """
    liste_couleurs = ['red', 'blue', 'green', 'yellow']
    hauteur = len(plan_plateau)
    largeur = len(plan_plateau[0])
    
    directions = [
        (-1, 0),  # haut
        (1, 0),   # bas
        (0, -1),  # gauche
        (0, 1)    # droite
    ]
    
    cases_liberees = 0
    
    for dl, dc in directions:
        nouvelle_ligne = ligne_centre + dl
        nouvelle_colonne = colonne_centre + dc
        
        if 0 <= nouvelle_ligne < hauteur and 0 <= nouvelle_colonne < largeur:
            if plan_plateau[nouvelle_ligne][nouvelle_colonne] == 2:
                plan_plateau[nouvelle_ligne][nouvelle_colonne] = 1
                cases_liberees += 1
                print("Jeton libéré à la position" +  str((nouvelle_ligne, nouvelle_colonne)))
                x1 = 100 + nouvelle_colonne * 50
                y1 = 100 + nouvelle_ligne * 50
                x2 = x1 + 50
                y2 = y1 + 50
                rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
                dessiner_jeton(x1, y1, x2, y2, 1, liste_couleurs)
    
    if cases_liberees > 0:
        print(str(cases_liberees) + " jeton(s) libéré(s) autour de la position " + str((ligne_centre, colonne_centre)))
    else:
        print("Aucun jeton à libérer autour de la position" + str((ligne_centre, colonne_centre)))
    
    return cases_liberees

def prendre_jeton(plan_plateau, x_clic, y_clic):
    """
    Fait disparaître un jeton si c'est un gros jeton (1)
    plan_plateau: le plan du plateau
    x_clic, y_clic: coordonnées du clic
    Retourne True si un jeton a été pris, False sinon
    """
    if not (100 <= x_clic <= 500 and 100 <= y_clic <= 600):
        return False
    
    colonne = (x_clic - 100) // 50
    ligne = (y_clic - 100) // 50
    
    if 0 <= ligne < len(plan_plateau) and 0 <= colonne < len(plan_plateau[0]):
        if plan_plateau[ligne][colonne] == 1:
            plan_plateau[ligne][colonne] = 4
            print("Jeton pris à la position" + str((ligne, colonne)))
            liste_couleurs = ['red', 'blue', 'green', 'yellow']
            x1 = 100 + colonne * 50
            y1 = 100 + ligne * 50
            x2 = x1 + 50
            y2 = y1 + 50
            
            rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
            
            liberation_jeton(plan_plateau, ligne, colonne)
            
            return True
        else:
            print("Case " + str((ligne, colonne)) + "- Pas un gros jeton (valeur: "+ str(plan_plateau[ligne][colonne]))
            return False
    else:
        return False

def parametre_fenetre():
    theme = input('Quelle couleur? ')
    cree_fenetre(1200,750)
    rectangle(0,0,1200,1200, remplissage=theme, couleur=theme)
    
    rectangle(650,100,1050,200, couleur='black', remplissage='white')
    texte(850, 150, "Pick Tok", taille=30, ancrage="center")
    
    rectangle(750,500,950,600, couleur='black', remplissage='white')
    texte(850, 525, "Score:", taille=10, ancrage="center")
    
    return theme


def generer_plan_plateau():
    plan_plateau = []
    
    for ligne in range(10):
        ligne_plan = []
        for colonne in range(8):
            if randint(0, 3) == 3:
                ligne_plan.append(0)
            else:
                if ligne == 0:
                    ligne_plan.append(1)
                else:
                    ligne_plan.append(2)
        plan_plateau.append(ligne_plan)
    
    return plan_plateau

def anti_isolation(plan_plateau, case_isolee):
    """
    Supprime une case isolée en transformant un mur adjacent en jeton
    plan_plateau: le plan du plateau
    case_isolee: tuple (ligne, colonne) de la case isolée
    """
    ligne, colonne = case_isolee
    hauteur = len(plan_plateau)
    largeur = len(plan_plateau[0])
    
    directions = []
    
    if ligne > 0 and plan_plateau[ligne-1][colonne] == 0:
        directions.append(('haut', ligne-1, colonne))
    if ligne < hauteur-1 and plan_plateau[ligne+1][colonne] == 0:
        directions.append(('bas', ligne+1, colonne))
    if colonne > 0 and plan_plateau[ligne][colonne-1] == 0:
        directions.append(('gauche', ligne, colonne-1))
    if colonne < largeur-1 and plan_plateau[ligne][colonne+1] == 0:
        directions.append(('droite', ligne, colonne+1))
    
    if directions:
        direction_choisie, ligne_mur, colonne_mur = directions[randint(0, len(directions)-1)]
        
        if ligne_mur == 0: 
            plan_plateau[ligne_mur][colonne_mur] = 1
        else:
            plan_plateau[ligne_mur][colonne_mur] = 2
        
        print("Mur supprimé en position " + str((ligne_mur,colonne_mur)) + "- direction" + str(direction_choisie))
        
        return True
    else:
        print("Aucune direction disponible pour supprimer l'isolation")
        return False

def verification_plateau(plan_plateau):
    detecter = False
    cases_isolees = []
    hauteur = len(plan_plateau)
    largeur = len(plan_plateau[0])
    
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if plan_plateau[ligne][colonne] in [1, 2]:
                murs_autour = 0
                
                if ligne == 0 or plan_plateau[ligne-1][colonne] == 0:
                    murs_autour += 1
                
                if ligne == hauteur-1 or plan_plateau[ligne+1][colonne] == 0:
                    murs_autour += 1
                
                if colonne == 0 or plan_plateau[ligne][colonne-1] == 0:
                    murs_autour += 1
                
                if colonne == largeur-1 or plan_plateau[ligne][colonne+1] == 0:
                    murs_autour += 1
                
                if murs_autour == 4:
                    detecter = True
                    cases_isolees.append((ligne, colonne))
                    print("Case isolée détectée à la position " + str((ligne, colonne)))
    
    if detecter:
        print(str(len(cases_isolees)) + "case(s) isolée(s) détectée(s) - correction en cours...")
        for case in cases_isolees:
            anti_isolation(plan_plateau, case)
    else:
        print("Aucune case isolée détectée")
    
    return detecter, plan_plateau


def generer_dessin_plateau(plan_plateau):
    liste_couleurs = ['red', 'blue', 'green', 'yellow']
    
    rectangle(95, 95, 505, 605, couleur='white', remplissage='white')
    
    x1 = 100
    y1 = 100
    x2 = 150
    y2 = 150
    
    for ligne in range(len(plan_plateau)):
        for colonne in range(len(plan_plateau[0])):
            if plan_plateau[ligne][colonne] == 0:
                rectangle(x1, y1, x2, y2, remplissage='black', couleur='black')
            else:
                rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
                dessiner_jeton(x1, y1, x2, y2, plan_plateau[ligne][colonne], liste_couleurs)
            
            x1 += 50
            x2 += 50
        
        x1 = 100
        x2 = 150
        y1 += 50
        y2 += 50
    
    x1 = 550
    y1 = 100
    x2 = 600
    y2 = 150
    
    for grille in range(5):
        rectangle(x1, y1, x2, y2, remplissage='white', couleur='black')
        y1 += 50
        y2 += 50


theme = parametre_fenetre()

plan_initial = generer_plan_plateau()
print("Plan initial généré:")
for ligne in plan_initial:
    print(ligne)

detecter, plan_valide = verification_plateau(plan_initial)

print("Plan après correction:")
for ligne in plan_valide:
    print(ligne)

generer_dessin_plateau(plan_valide)

while True:
    ev = donne_ev()
    tev = type_ev(ev)
    
    if tev == 'Quitte':
        break
    elif tev == "ClicGauche":
        x_clic = abscisse(ev)
        y_clic = ordonnee(ev)
        print("Clic gauche au point", (x_clic, y_clic))
        prendre_jeton(plan_valide, x_clic, y_clic)
    
    mise_a_jour()

attend_fermeture()