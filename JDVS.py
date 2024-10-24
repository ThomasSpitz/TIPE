import random as rd
import pygame
import numpy as np
from pygame.locals import *
import scipy.signal

from affichages import *

##Options d'éxecution

size = 100
manuel = True
p=0.72
barrieres=False
afficher_entropie=True
afficher_mass=True
afficher_temp=True
lisser_courbe= False

##Variables globales

ratio = 1000/size
cycle = 0
Mass=[0]
Entropy=[0]
Temp=[0]
Temp2=[0]
field = [[0 for i in range (size+2)] for j in range (size+2)]
entropie = [[0 for i in range (size+2)] for j in range (size+2)]
temp = [[0 for i in range (size+2)] for j in range (size+2)]


##Fonctions règles

def rules1(neighbor):
    entropy=0

    if sum(neighbor)>=2 and sum(neighbor)<=3 and neighbor[4]>0:
        entropy-=0.6*np.log2(0.6)
    elif sum(neighbor)>=2 and sum(neighbor)<=3 and neighbor[4]==0:
        entropy-=0.4*np.log2(0.4)
    elif sum(neighbor)>0 :
        entropy-=0.2*np.log2(0.2)
    
    r = rd.randint(1,10)
    if sum(neighbor)>=2 and sum(neighbor)<=3 and r<=6 and neighbor[4]>0:
        return rd.uniform(0,neighbor[4]),entropy
    elif sum(neighbor)>=2 and sum(neighbor)<=3 and neighbor[4]==0 and r<=4:
        return rd.uniform(0,sum(neighbor)/4),entropy
    elif r>=9 and sum(neighbor)>0 :
        return rd.uniform(neighbor[4],1),entropy
    else:
        return 0,entropy
    
def rules2(neighbor):
    global p
    r=rd.randint(1,100)
    if neighbor[4]>0 and (sum(neighbor)<0.+neighbor[4] or sum(neighbor)>2.5 + neighbor[4]):
        if r>=(p*100) :
            return neighbor[4],-0.2*np.log2(0.2)
        else:
            return 0,(p-1)*np.log2(1-p)
    elif neighbor[4]>0:
        if r>=(p*100):
            return 0,(p-1)*np.log2(1-p)
        else:
            return neighbor[4],(p-1)*np.log2(1-p)
    elif neighbor[4]==0 and sum(neighbor)>=0.5 and sum(neighbor)<=2.5 + neighbor[4]:
        if r<=(p*100) :
            return rd.uniform(0,min(sum(neighbor),1)),-p*np.log2(p)
        else:
            return 0,-p*np.log2(p)
    else : 
        return 0,0
    
def rules3(neighbor):
    global p
    r=rd.uniform(0,1)
    s=sum(neighbor)-neighbor[4]
    if neighbor[4]==0 :         #cas ou la cellule est morte
        if s==0:
            return 0,0
        elif s>=1.5 and s<=2.5 :
            if r<=p:        
                return rd.uniform(0,0.5),-p*np.log(p)
            else:
                return 0,-p*np.log(p)
        else :
            if r<=p:
                return 0,(p-1)*np.log(1-p)
            else:
                return rd.uniform(0,0.5),(p-1)*np.log(1-p)
    else:                       #cas ou la cellule est vivante
        if s>=1.5 and s<=3.5 :
            if r<=p:        
                return neighbor[4],-p*np.log(p)
            else:
                return 0,-p*np.log(p) 
        else:    
            if r<=p:
                return 0,(p-1)*np.log(1-p)
            else:
                return neighbor[4],(p-1)*np.log(1-p)       


##Fonction d'affichage de la grille

def afficher(field,background):
    for i in range(1,size+1):
        for j in range(1,size+1):
            if barrieres:
                if i==50 and j!=size/2 and j!=size/2-1 and j!=size/2-1:
                    pygame.draw.rect(background,(0,0,0),Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
                else :
                    pygame.draw.rect(background,(255,255*(1-field[i][j]),255*(1-field[i][j])),Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
            else :
                pygame.draw.rect(background,(255,255*(1-field[i][j]),255*( 1-field[i][j])),Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))



##Fonction d'actualisation

def refresh (temp,entropie,rules,field,background):
    newfield = [[0 for i in range (size+2)] for j in range (size+2)]
    newentropie = [[0 for i in range (size+2)] for j in range (size+2)]
    
    for i in range(1,size+1):
        for j in range(1,size+1):

            if i==50 and j!=size/2 and j!=size/2-1 and j!=size/2-1 and barrieres:
                continue

            else :
                newfield[i][j],newentropie[i][j]=rules([field[x][y] for x in range(i-1,i+2) for y in range(j-1,j+2)])
                
                if(entropie[i][j]!=newentropie[i][j]):                     
                    temp[i][j]=(newfield[i][j]-field[i][j])/(newentropie[i][j]-entropie[i][j])                  ##formule T=dE/dS

    afficher(field,background)
    return newfield,newentropie,temp


##Fonctions d'initialisation : aléatoire et manuelle

def randominit(field,screen,background):
    for i in range(size//3,2*size//3):
        for j in range(size//3,2*size//3):
            field[i][j]=1
    afficher(field,background)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def init_manuel(field,screen,background):
    field[size//2][size//2]=1
    afficher(field,background)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    done=False
    while not done :
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN :
                (x,y) = pygame.mouse.get_pos()
                (x,y) = (int(x//ratio)+1,int(y//ratio)+1)
                if x!=0 and x!=size+1 and y!=0 and y !=size+1 and x!=size/2:
                    field[x][y]=(field[x][y] + 0.2)%1.2
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:    
                done=True

            afficher(field,background)
            screen.blit(background, (0, 0))
            pygame.display.flip()  



##Fonction main

def main():

    global cycle
    global Mass
    global Entropy
    global Temp
    global Temp2
    global field
    global entropie
    global temp


    ##Initialisation de la fenêtre pygame

    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(((255,255,255)))

    initfic()

    if not manuel :
        randominit(field)
    else:
        init_manuel(field,screen,background)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        
        dt = clock.tick(10)

        ##Mise à jour des valeurs

        field,entropie,temp=refresh(temp,entropie,rules3,field,background)
        
        ecriture(field,"mass.csv",size)
        ecriture(entropie,"entropie.csv",size)
        ecriture(temp,"temperature.csv",size)

        Mass.append(sum(field[x][y] for x in range (1,size+1) for y in range (1,size+1)))
        Entropy.append(sum(entropie[x][y] for x in range (1,size+1) for y in range (1,size+1)))
        Temp.append((sum(temp[x][y] for x in range (1,size+1) for y in range (1,size+1)))/(size+1)**2)
        Temp2.append((Mass[-1]-Mass[-2])/(Entropy[-1]-Entropy[-2]) if Entropy[-1]-Entropy[-2]!=0 else Temp2[-1])

        screen.blit(background, (0, 0))
        pygame.display.flip()
        cycle+=1
        print(cycle)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(sum(Temp)/cycle)
                print(sum(Temp2)/cycle)
                pygame.quit()
                if afficher_entropie:
                    graphe(Entropy,"Entropie")
                if afficher_mass:
                    graphe(Mass,"Masse")
                if afficher_temp:
                    graphe(Temp,"Température (à partir de calculs locaux)")
                    graphe(Temp2,"Température (à partir de calculs globaux)")


                if lisser_courbe == True :
                    if afficher_entropie:
                        graphe(scipy.signal.savgol_filter(Entropy,cycle,10),"Entropie")
                    if afficher_mass:
                        graphe(scipy.signal.savgol_filter(Mass,cycle,10),"Masse")
                    if afficher_temp:
                        graphe(scipy.signal.savgol_filter(Temp2,cycle,7),"Température (à partir de calculs locaux)")
                        graphe(scipy.signal.savgol_filter(Temp2,cycle,7),"Température (à partir de calculs globaux)")
                plt.show()                  

            
if __name__ == '__main__': main()



