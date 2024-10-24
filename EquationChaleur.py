import numpy as np
import matplotlib.pyplot as plt
from affichages import *
import time

##Options d'éxecution

size = 100


##Variables globales

S_val = 2000
rho = 10.5e3 
Cp = 0.235
l = 420

dt = 1e-2  ##pas de la simulation
dx = 1
dy = 1

##Permettent les dérivées temporelles
T_old = np.zeros(
    (size + 2, size + 2)
)  # Tableau contenant les valeurs de températures anciennes
T_new = np.zeros(
    (size + 2, size + 2)
)  # Tableau contenant les valeurs de températures nouvelles

S_tab = np.zeros(
    (size + 2, size + 2)
)  # Tableau indiquant si la case est un terme de source


##Initialisation de S_tab

S_tab[size // 2][size // 2] = 1
S_tab[size // 2 + 1][size // 2] = 1
S_tab[size // 2][size // 2 + 1] = 1
S_tab[size // 2 + 1][size // 2 + 1] = 1

##Fonction d'actualisation : méthode d'Euler


def actualiser(T_old, T_new, S_tab):
    global dt, dx, dy, S_val, rho, Cp, l
    for x in range(1, size + 1):
        for y in range(1, size + 1):
            T_new[x][y] = T_old[x][y] + dt / rho / Cp * (
                l * (T_old[x + 1][y] + T_old[x - 1][y] - 2 * T_old[x][y]) / (dx**2)
                + l * (T_old[x][y + 1] + T_old[x][y - 1] - 2 * T_old[x][y]) / (dy**2)
            )
            if S_tab[x][y]:
                T_new[x][y] += dt / rho / Cp * S_val
    return T_new


cycle = 0


fichier = open("theorique.csv", "w")
fichier.close()
T=[0]
while True:
    T_old = actualiser(T_old, T_new.copy(), S_tab)
    T.append((sum(T_old[x][y] for x in range (1,size+1) for y in range (1,size+1)))/(size+1)**2)
    if cycle%10000== 0:
        print(cycle*dt)
        ecriture(T_old, "theorique.csv", size)
    cycle = cycle + 1
