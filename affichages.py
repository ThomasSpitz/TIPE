import numpy as np
import matplotlib.pyplot as plt


##Fonctions d'écriture

def initfic():
    fichier=open("mass.csv","w")
    fichier.close()
    fichier=open("entropie.csv","w")
    fichier.close()
    fichier=open("temperature.csv","w")
    fichier.close()

def ecriture(tab,nom,size):
    fichier = open(nom, "a")
    for i in range(1,size+1):
        for j in range(1,size+1):
            fichier.write(str(tab[i][j])+";")
    fichier.write("\n")
    fichier.close()

##Fonction de lecture (prend le fichier et le cycle et renvoie le tableau unidimensionnel correspondant)

def lire(fic, cycle):
    f = open(fic,"r")
    line=f.readlines()[cycle]
    f.close()
    return line.split(";")


def passagea2d(tab,size):
    new=[[0]*size for i in range (size)]
    for i in range(size):
        for j in range(size):
            new[i][j]=float(tab[i*size+j])
    return new

##Afficher cartes

def map(fic,cycle,size):
    X = passagea2d(lire(fic,cycle),size)

    fig = plt.figure(figsize=(8, 6))
    plt.imshow(X, cmap='viridis')
    plt.title("Température")
    plt.colorbar()


def graphe(donnee,nom):
    plt.figure(nom)
    plt.plot(donnee)
    plt.xlabel("Nombre de cycles (divisé par 10000)")
    plt.ylabel(nom)
    plt.title(nom+" en fonction du temps")
