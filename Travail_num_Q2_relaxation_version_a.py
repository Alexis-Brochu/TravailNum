#Travail numérique ÉlectroMagnétisme H2024
#William Boissonneault (537 xxx xxx)
#Alexis Gagné-Brochu (537 xxx xxx)
#2024-04-26

import numpy as np
import matplotlib.pyplot as plt
import fonctions_utiles as fu
import time


#Nous travaillerons toujours en m, le tout sera transformé en mm lors de l'affichage
#des figures

#INITIALISATION
start_time = time.time()    #Commence chronomètre
h = 0.0001   #agit comme ''Résolution'' de relaxation 

#Création du ''monde''
hauteur_monde_z = 0.012
largeur_monde_r = 0.003
z = np.arange(0, hauteur_monde_z + h, h)
r = np.arange(0, largeur_monde_r + h, h)
Z, R = np.meshgrid(z, r)

#Matrice de test pour tester affichage de matrice
#TODO: REMOVE C'EST QUE POUR TEST
Matrice_monde = Z + R
#                 R   Z
#V_test_affichage[1][10] = 10

def Construire_Matrice_CF(Matrice_monde) :
    """Cette fonction crée une matrice numpy 2D avec la géométrie du problème,
    La valeur de condition est inscrite, si le noeud n'est pas fixe, la valeur np.nan
    est inscrite"""
    #TODO: Pour visualisation, pour calculs mettre np.nan
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
    for i in range(1,index_max_parois_sup): #1 pour ne pas mettre de valeur au coin supp
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

def maintient_des_CF(V_in, Mactrice_CF):
    """Cette fonction applique les conditions frontières sur une matrice d'entrée"""

    ###TODO: peut etre plus rapide d'avoir une liste de CF et non matrice entière
    mask = ~np.isnan(Matrice_CF)
    V_in[mask] = Mactrice_CF[mask]
    
    return V_in

def Initialisation_Vactuel(Matrice_monde, Matrice_CF) :
    """Cette fonction crée la première matrice numpy 2D du potentiel actuel,
    Les valeurs de potentiel en tout point est mise"""

    ###Nous commençons à -150 pour acceleré la convergance (PAS CERTAIN SI CA LE FAIT POUR VRAI)
    V_debut = np.ones_like(Matrice_monde) * -50
    V_debut = maintient_des_CF(V_debut, Matrice_CF)

    return V_debut

def Relaxation_simple(V_actuel, Matrice_CF) :
    """Cette fonction effectue une étape de Relaxation et retourne la nouvelle
    matrice du potentiel actuel et un indice du changements effectuté"""
    
    M_Vactuel_gauche = V_actuel[::]
    M_Vactuel_droite = V_actuel[::]
    M_Vactuel_haut = V_actuel[::]
    M_Vactuel_bas = V_actuel[::]

    #TODO utiliser vraie mathématique
    V_nouveaux = 0.25 * (M_Vactuel_gauche + M_Vactuel_droite + M_Vactuel_haut + M_Vactuel_bas) + Facteur_cylindrique

    #Replacemnt dans condtions frontières
    V_nouveaux = V_nouveaux + Matrice_CF

    #Indice de changement pour condition de fin
    Indice_changement = np.average(V_actuel) - np.average(V_nouveaux)

    return V_nouveaux, Indice_changement


def affichage_de_matrice(Matrice_V, nom_fichier=False) :
    """Cette fonction affiche la matrice de potentiel passée en entrée
    Utile pour débogger ET pour la production de figure finale"""

    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(111)

    #Nous transformons en mm pour une bonne lecture
    contour = ax.contourf(Z * 1000, R * 1000, Matrice_V, cmap='viridis', levels=10000)
    ax.set_aspect('equal')

    cbar = fig.colorbar(contour, ax=ax, label='Potentiel électrique V [V]', location="left", shrink=0.6)
    ax.set_xlabel('Position en z (mm)')
    ax.set_ylabel('Position radiale (mm)')
    ax.grid(True)

    #inverse l'axe des z pour pouvoir illustrer comme la figure de l'énoncé
    ax.invert_xaxis()

    

    #Positionnement des élements visuelle
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    cbar.ax.yaxis.set_label_position('left')

    plt.subplots_adjust(left=0, right=0.9, top=1, bottom=0, wspace=0.2, hspace=0.2)

    plt.show()

###Operations###

Matrice_CF = Construire_Matrice_CF(Matrice_monde)

V_actuel = Initialisation_Vactuel(Matrice_monde, Matrice_CF)

#Relaxation_en_cours = True

#i=0
#while(Relaxation_en_cours):
#    V_nouveaux, Indice_changement = Relaxation_simple(V_actuel, Matrice_CF)

#    print(f"Relaxation {i} effectué, indice de changement : {Indice_changement}")
    ###Condition d'arrêts:
#    if (Indice_changement < cond_arret){
#        Relaxation_en_cours = False
#    }
#    i += 1


print("Programme executé en --- %s seconds ---" % (time.time() - start_time))
affichage_de_matrice(Matrice_monde, nom_fichier="nom_de_figure")
affichage_de_matrice(Matrice_CF, nom_fichier="nom_de_figure")
affichage_de_matrice(V_actuel, nom_fichier="nom_de_figure")

