##Python Jeu de la vie Classique

import random as rd
import pygame
from pygame.locals import *


size = 40
ratio = 800/size
random=True
masse_max = 1

def classic (neighbor):
    if neighbor[4]==1 and (sum(neighbor)==3 or  sum(neighbor)==4) :
        return 1
    elif neighbor[4]==0 and sum(neighbor)==3 :
        return 1
    else:
        return 0

def refresh (rules,field,background):
    newfield = [[0 for i in range (size+2)] for j in range (size+2)]
    for i in range(1,size+1):
        for j in range(1,size+1):
            newfield[i][j]=rules([field[x][y] for x in range(i-1,i+2) for y in range(j-1,j+2)])
            if newfield[i][j]!=field[i][j]:
                if newfield[i][j]==1:
                    pygame.draw.rect(background,"black",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
                else :
                    pygame.draw.rect(background,"white",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
    return newfield

def afficher(field,background):
    for i in range(size+2):
        for j in range(size+2):
            if field[i][j]==1:
                pygame.draw.rect(background,"black",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
            elif field[i][j]==2:
                pygame.draw.rect(background,"red",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
            elif field[i][j]==3:
                pygame.draw.rect(background,"blue",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
            elif field[i][j]==4:
                pygame.draw.rect(background,"green",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))
            else :
                pygame.draw.rect(background,"white",Rect((i-1)*ratio,(j-1)*ratio,ratio,ratio))

def randominit(field):
    for i in range(1,size + 1):
        for j in range(1,size + 1):
            field [i][j]=rd.randint(0,1)


def main():
    clock = pygame.time.Clock()
    field = [[0 for i in range (size+2)] for j in range (size+2)]
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption('')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill('white')
    
    if random :
        randominit(field)
        afficher(field,background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
    
    else :
        done=False
        while not done :
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN :
                    (x,y) = pygame.mouse.get_pos()
                    (x,y) = (int(x//ratio)+1,int(y//ratio)+1)
                    if x!=0 and x!=size+1 and y!=0 and y !=size+1:
                        field[x][y]=(field[x][y] + 1) % 5
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:    
                    done=True

                afficher(field,background)
                screen.blit(background, (0, 0))
                pygame.display.flip()

    screen.blit(background, (0, 0))
    
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        dt = clock.tick(10)
        field=refresh(classic,field,background)          
        
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': main()