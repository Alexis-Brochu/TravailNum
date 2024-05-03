#Travail numérique ÉlectroMagnétisme H2024
#William Boissonneault (537 xxx xxx)
#Alexis Gagné-Brochu (537 xxx xxx)
#2024-04-26

import numpy as np
import matplotlib.pyplot as plt
import fonctions_utiles as fu
import time

####ATTENTION, CE FICHIER CALCULE PLUSIEURS FOIS LA MEME NUMERO
####NOUS VOLUONS CHARACTERISER LE TEMPS pour arriver à une réponse

#Nous travaillerons toujours en m, le tout sera transformé en mm lors de l'affichage
#des figures

#INITIALISATION
h = 0.0001   #agit comme ''Résolution'' de relaxation 

#Création du ''monde''
hauteur_monde_z = 0.012
largeur_monde_r = 0.003
###Pour pouvoir utiliser calcul matricielle optimisé, nous ajoutons une rangé à r=-h
###Qui ne sera PAS calculé puisqu'elle est sur un bord
z = np.arange(0, hauteur_monde_z + h, h)
r = np.arange(0, largeur_monde_r + h, h)
Z, R = np.meshgrid(z, r)

#Matrice de test pour tester affichage de matrice et pour avoir une matrice monde 
#de la bonne grosseur
Matrice_monde = Z + R
#                 R   Z
#V_test_affichage[1][10] = 10

def Construire_Matrice_CF(Matrice_monde) :
    """Cette fonction crée une matrice numpy 2D avec la géométrie du problème,
    La valeur de condition est inscrite, si le noeud n'est pas fixe, la valeur np.nan
    est inscrite"""
    Matrice_CondF = np.ones_like(Matrice_monde) * np.nan
    shape = np.shape(Matrice_CondF)

    V_1 = 0 #potentiel électrode 1
    V_2 = -300 #potentiel surfaces

    l_electrode_centrale = 0.0075
    index_max_electrode = int((l_electrode_centrale / hauteur_monde_z) * shape[1]) + 1

    l_parois_sup = 0.009
    index_max_parois_sup = int((l_parois_sup / hauteur_monde_z) * shape[1]) + 1

    ###Plaque au fond (z=0) à V_1 ###
    for i in range(shape[0]-1): #-1 pour ne pas mettre de valeur au coin supp
        Matrice_CondF[i][0] = V_1

    ###Électrode centrale (r=0) à V_1 ###
    for i in range(index_max_electrode): 
        Matrice_CondF[0][i] = V_1

    ###Parois supérieur (r=3mm) ###
    for i in range(index_max_parois_sup): #1 pour ne pas mettre de valeur au coin supp
        Matrice_CondF[shape[0]-1][i] = V_2

    ###Parois en angle, fonctionne que pour une angle de 45deg###
    i=0
    while True:
        try:
            Matrice_CondF[i][shape[1]-1-i] = V_2
            i+=1
        except IndexError:
            break

    return Matrice_CondF

def Initialisation_Vactuel(Matrice_monde, Matrice_CF, mask_CF) :
    """Cette fonction crée la première matrice numpy 2D du potentiel actuel,
    Les valeurs de potentiel en tout point est mise"""

    ###Commence tout à 0
    V_debut = np.ones_like(Matrice_monde) * 0
    ###Applique condition frontières
    V_debut[mask_CF] = Matrice_CF[mask_CF]

    return V_debut

def Relaxation_simple(V_actuel, Matrice_CF, mask_CF) :
    """Cette fonction effectue une étape de Relaxation et retourne la nouvelle
    matrice du potentiel actuel et un indice du changements effectuté"""

    ###Nous prenons une sous-partie de la matrice actuelle pour pouvoir 
    ###faire la moyenne en tout point gauche, droite, haut, bas
    ###(pas vraiment tout point, les bordures ne sont jamais changé)

    moyenne_init = np.average(V_actuel)
    
    M_Vactuel_gauche = V_actuel[:-2,1:-1]
    M_Vactuel_droite = V_actuel[2:,1:-1]
    M_Vactuel_haut = V_actuel[1:-1,:-2]
    M_Vactuel_bas = V_actuel[1:-1,2:]

    #TODO utiliser vraie mathématique avec facteur cylindrique
    V_nouveaux = ((M_Vactuel_gauche + M_Vactuel_droite + M_Vactuel_haut + M_Vactuel_bas) / 4 ) + (h/8) * (M_Vactuel_gauche + M_Vactuel_droite)

    #Écrasement du centre de la matrice
    V_actuel[1:-1,1:-1] = V_nouveaux

    #Changement de la ligne à r=0 avec l'équation 1b)
    V_actuel[0,1:-1] = 0.5 * (V_actuel[0,0:-2]+V_actuel[0,2:])

    #Replacemnt des condtions frontières
    V_actuel[mask_CF] = Matrice_CF[mask_CF]

    Indice_changement = moyenne_init - np.average(V_actuel)

    return V_actuel, Indice_changement


def affichage_de_matrice(Matrice_V, nom_fichier=False, mask_actif=False) :
    """Cette fonction affiche la matrice de potentiel passée en entrée
    Utile pour débogger ET pour la production de figure finale"""

    #Pas optimisé, est seulement utiliser pour avoir une belle affichage
    if mask_actif:
        i=1
        while True:
            try:
                for j in range(1,i+1):
                    Matrice_V[i][-j] = np.nan
                i+=1
            except IndexError:
                break

    fig = plt.figure(figsize=(8, 2.5))
    ax = fig.add_subplot(111)

    #Nous transformons en mm pour une bonne lecture
    contour = ax.contourf(Z * 1000, R * 1000, Matrice_V, cmap='viridis', levels=100)
    ax.set_aspect('equal')

    cbar = fig.colorbar(contour, ax=ax, label='Potentiel électrique [V]', location="left", shrink=0.7, pad=0.05)
    ax.set_xlabel('Position en z [mm]')
    ax.set_ylabel('Position radiale [mm]')
    ax.grid(True)

    #inverse l'axe des z pour pouvoir illustrer comme la figure de l'énoncé
    ax.invert_xaxis()

    #Positionnement des élements visuelle
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    cbar.ax.yaxis.set_label_position('left')
    cbar.set_ticks(np.linspace(0, -300, 7))

    plt.subplots_adjust(left=0, right=0.9, top=1, bottom=0, wspace=0.2, hspace=0.2)

    plt.savefig('Potentiel_Relaxation_2_a.png', dpi=600)
    plt.show()

###Operations###

temps_necessaire = []
iterations_necessaire = []
for j in range(100):
    start_time = time.time()    #Commence chronomètre
    Matrice_CF = Construire_Matrice_CF(Matrice_monde)
    mask_CF = ~np.isnan(Matrice_CF)

    V_actuel = Initialisation_Vactuel(Matrice_monde, Matrice_CF, mask_CF)

    Indice_changement = []
    iterations = []

    i=0
    while True:
        V_actuel, Indice_changement_i = Relaxation_simple(V_actuel, Matrice_CF, mask_CF)
        Indice_changement.append(Indice_changement_i)
        iterations.append(i)

        if Indice_changement_i == 0 or i > 15000:
            break
        i+=1

    ### On arrête le temps 
    temps_necessaire.append(time.time() - start_time)
    iterations_necessaire.append(i)

###Calculs de temps et d'itération 
temps_necessaire = np.array(temps_necessaire)
iterations_necessaire = np.array(iterations_necessaire)

#Valeurs finales
print(f"Avec l'ordinateur utilisé le temps necessaire est de")
print(f"{np.average(temps_necessaire)} +- {2*np.std(temps_necessaire)} sec.")
print(f"Avec l'ordinateur utilisé le nombre d'itérations est de")
print(f"{np.average(iterations_necessaire)} +- {2*np.std(iterations_necessaire)}")

###On affiche la figure final
affichage_de_matrice(V_actuel, nom_fichier="nom_de_figure", mask_actif = True)

###Affichage de la figure pour c)
fig = plt.figure(figsize=(8, 3))
plt.subplots_adjust(left=0.1, right=0.98, top=1, bottom=0.16, wspace=0.2, hspace=0.2)
plt.plot(
    iterations,Indice_changement
)
plt.xlabel("Nombre d'itérations [-]")
plt.ylabel("Variation de la moyenne [V]")
plt.yscale("log")
plt.savefig("Graphique_condition_arret",dpi=600)
plt.show()
