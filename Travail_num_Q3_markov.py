#Travail numérique Électromagnétisme H2.024
#William Boissonneault (537 032 683)
#Alexis Gagné-Brochu (537 163 545)
#2024-04-26
import numpy as np

#initialisation de la matrice R
MatriceR = np.zeros((9, 13), dtype=float)

MatriceR[0, 4] = .5 ; MatriceR[2, 5] = .5 ; MatriceR[3, 6] = .249906285143 ; MatriceR[3, 7] = .250093714857
MatriceR[4, 8] = .250093714857 ; MatriceR[5, 4] = .250093714857 ; MatriceR[5, 9] = .250093714857
MatriceR[6, 3] = .250093714857 ; MatriceR[6, 10] = .250093714857 ; MatriceR[7, 2] = .250093714857 ;MatriceR[7, 11] = .250093714857
MatriceR[8, 0] = .249906285143 ; MatriceR[8, 1] = .250093714857 ; MatriceR[8, 12] = .250093714857

#initialisation de la matrice Q
MatriceQ = np.zeros((9, 9), dtype=float) 

MatriceQ[0, 1] = .5 ; MatriceQ[1, 0] = .5 ; MatriceQ[1, 2] = .5 ; MatriceQ[2, 1] = .5 ; MatriceQ[3, 1] = .250093714857
MatriceQ[3, 4] = .249906285143 ; MatriceQ[4, 0] = .250093714857 ; MatriceQ[4, 3] = .249906285143 ; MatriceQ[4, 5] = .249906285143
MatriceQ[5, 4] = .249906285143 ; MatriceQ[5, 6] = .249906285143 ; MatriceQ[6, 5] = .249906285143 ; MatriceQ[6, 7] = .249906285143
MatriceQ[7, 6] = .249906285143 ; MatriceQ[7, 8] = .249906285143 ; MatriceQ[8, 7] = .249906285143

#initialisation du vecteur V_r (Vecteur des conditions frontières)
VecteurV_r = np.zeros((13, 1))

VecteurV_r[5, 0] = -300 ; VecteurV_r[6, 0] = -300 ; VecteurV_r[7, 0] = -300 ; VecteurV_r[8, 0] = -300 
VecteurV_r[9, 0] = -300 ; VecteurV_r[10, 0] = -300 ; VecteurV_r[11, 0] = -300 ; VecteurV_r[12, 0] = -300


#Création de la matrice I_t
MatriceI_t = np.eye(9)

#Calcul du nombre moyen de passages
MatriceN = np.linalg.inv(MatriceI_t-MatriceQ)

#Calcul de la matrice B
MatriceB = np.dot(MatriceN, MatriceR)

#Calcul de la matrice Vt
Matrice_Vt = np.dot(MatriceB, VecteurV_r)

#Affichage du potentiel aux noeuds transitoires (dans l'ordre ; de 1 à 9)
print(Matrice_Vt)