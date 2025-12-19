import fltk
def traiter_fichier_txt(chemin_fichier):
    #transformer le contenu de "texte.txt" en liste

    with open(chemin_fichier,"r") as texte:
        contenu = texte.read()
    liste = eval(contenu)
    return liste
def taille_fenetre(Hauteur = 750 , Largeur = 1200) :
    return (Hauteur , Largeur)

def creation_leaderboard(Hauteur , Largeur) :
    #création fond ( on pourrait ajouter une image )
    fltk.rectangle(0,0,Largeur,Hauteur,couleur = "black",epaisseur = 5,remplissage = "#ffffff")
    fltk.rectangle((Largeur/2)-75,Hauteur-100,(Largeur/2)+75,Hauteur-50,couleur = "black",epaisseur = 2,remplissage = "#ab437e")
    fltk.texte((Largeur/2),Hauteur-75,"Menu", taille = 24, ancrage ='center')
    fltk.texte((Largeur/2), 100, "Classement", taille= 36, ancrage='center')


#définir nouveau top 50, réorganiser liste
def trouver_top_50(liste):
    liste_top_50 = []
    for i in range (min(len(liste),50)):
        indice = 0
        for i in range (len(liste)):
            if liste[i][1] >= liste[indice][1]:
                indice = i
        liste_top_50.append(liste[indice])
        liste.pop(indice)
    return(liste_top_50)

"""
faire un liste.append("nom du joueur",score de la partie ici",merci d'avance)
"""

#afficher le top 5

def top_5(Hauteur , Largeur , top_50):
    for i in range (min(5,len(top_50))):
        couleurs = ["#f2c64e","#9e9e9e","#754f23","#000000","#000000"]
        fltk.texte((Largeur/2) -75 ,200 + (50*i),top_50[i][0], taille  = 14,couleur = couleurs[i],ancrage = "center")
        fltk.texte((Largeur/2) +75 ,200 + (50*i),top_50[i][1], taille  = 14,couleur = couleurs[i],ancrage = "center")
    
#récrire le fichier texte
def ajouter_scores_txt(chemin_fichier , top_50) :
    with open(chemin_fichier, "w") as texte:
        texte.write(str(top_50))
def actualiser_top_50(liste_top_50, pseudo, score_joueur):
    # 1. On ajoute le nouveau joueur à la fin de la liste
    nouveau_score = [pseudo, score_joueur]
    liste_top_50.append(nouveau_score)
    
    # 2. On trie la liste par ordre décroissant (Tri par insertion simplifié)
    # On fait "remonter" le dernier élément tant qu'il est plus grand que celui d'avant
    i = len(liste_top_50) - 1
    while i > 0:
        # Si le score actuel est plus grand que le score précédent
        if liste_top_50[i][1] > liste_top_50[i-1][1]:
            # On échange les deux places
            liste_top_50[i], liste_top_50[i-1] = liste_top_50[i-1], liste_top_50[i]
            i = i - 1
        else:
            # Si le score n'est pas plus grand, il est à sa place, on arrête
            break
            
    # 3. Si la liste dépasse 50 éléments, on enlève le dernier (le plus faible)
    if len(liste_top_50) > 50:
        liste_top_50.pop() # Enlève le dernier élément
        
    return liste_top_50
def main_leaderboard(score_joueur , pseudo) :
    Taille_fenetre = taille_fenetre()
    liste = traiter_fichier_txt("classement.txt")
    liste_top_50 = trouver_top_50(liste)
    liste_top_50 = actualiser_top_50(liste_top_50, pseudo, score_joueur)
    ajouter_scores_txt("classement.txt", liste_top_50)
    creation_leaderboard(Taille_fenetre[0] , Taille_fenetre[1])
    top_5(Taille_fenetre[0] , Taille_fenetre[1] , liste_top_50)
    fltk.mise_a_jour()

    # Cliquer pour fermer

    ev = fltk.attend_ev()

    typeEV = fltk.type_ev(ev)

    if typeEV == "ClicGauche":
        x,y = fltk.abscisse(ev),fltk.ordonnee(ev)
    if ((Taille_fenetre[1]/2)-75 < x < (Taille_fenetre[1]/2)+75) and (Taille_fenetre[0]-100  < y < Taille_fenetre[0]-50):
        fltk.ferme_fenetre()


    

    

    

 

