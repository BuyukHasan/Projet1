from fltk import*
from random import randint
theme = input('Quelle couleur?')
cree_fenetre(1200,750)
rectangle(0,0,1200,1200, remplissage = theme,couleur = theme)
rectangle(650,100,1050,200,couleur = 'black', remplissage = 'white')
texte(850, 150, "Pick Tok", taille=30, ancrage="center",)
rectangle(750,500,950,600,couleur = 'black', remplissage = 'white')
texte(850, 525, "Score:", taille=10, ancrage="center",)
liste_couleurs = ['red','blue','green','yellow']
rectangle(95,95,505,605,couleur = 'white', remplissage = 'white')
alea = randint(9,18)
nb_bleu = alea - (alea%3)
labyrinthe = []
x1 = 550
y1 = 100
x2 = 600
y2 = 150
for grille in range(5):
    rectangle(x1,y1,x2,y2, remplissage = 'white', couleur = 'black')
    y1 = y1 + 50
    y2 = y2 + 50  
x1 = 100
y1 = 100
x2 = 150
y2 = 150
for colonne in range (10):
    for ligne in range(8):
        if randint(0,3)==3:
            rectangle(x1,y1,x2,y2, remplissage = 'black', couleur = 'black' )
            labyrinthe.append('mur')
        else:
            rectangle(x1,y1,x2,y2, remplissage = 'white', couleur = 'black')
            cercle((x1 + x2)/2,(y1 + y2)/2,20, couleur = 'black', )
            if colonne == 0:
                couleure = liste_couleurs[randint(0,3)]
                cercle((x1 + x2)/2,(y1 + y2)/2,20, couleur = 'black',remplissage = couleure  )
                labyrinthe.append((couleure,'C'))
            else:
                couleure = liste_couleurs[randint(0,3)]
                cercle((x1 + x2)/2,(y1 + y2)/2,10, couleur = 'black',remplissage = liste_couleurs[randint(0,3)]  )
                labyrinthe.append((couleure,'NC'))
                         
        x1 = x1 + 50
        x2 = x2 + 50
    
    x1 = x1 - 400
    x2 = x2 - 400
    y1 = y1 + 50
    y2 = y2 + 50
labyrinthe1 = [labyrinthe[i:i+8] for i in range(0,len(labyrinthe)-8 , 8)]
detecter = False
#for lignes in range(0,len(labyrinthe1)) :
   # for colonne in range(0, len(labyrinthe1[0])) :

       # if (lignes != 0) and (lignes != len(labyrinthe1) - 1) and (colonne != 0 )and (colonne != len(labyrinthe1[0])) :
           # if (labyrinthe1[lignes][colonne+1] == 'mur') and (labyrinthe1[lignes][colonne-1] == 'mur') and (labyrinthe1[lignes+1][colonne] == 'mur') and (labyrinthe1[lignes-1][colonne] == 'mur'):
               # detecter = True
        
        
if detecter == True :
   print("case isolée detectée")
print(labyrinthe1)
attend_fermeture()

