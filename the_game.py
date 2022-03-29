import time 
import os
import pygame 
pygame.init()

#estado do tabuleiro 
N = 8 #tamanho do tabuleiro 
size = 600 #tamanho da janela 
sq = (size/N) #tamanho da celula 
Ntabs = 6 #numero de ficheiros de tabuleiros 
nMovs = 0
fich = "fich.txt" #nome do ficheiro com os mapas

tab = []
tabcopia = []


class moves:
    xi = 0
    yi = 0
    xf = 0
    yf = 0
    player = 0
    tipo = 0


def copia():
    for i in range(N):
        for j in range(N):
            tabcopia[j][i] = tab[j][i]   


def restaurar():
    for i in range(N):
        for j in range(N):
            tab[i][j] = tabcopia[j][i]


#dado o jogador atual, retorna o outro jogador 
def otherplayer():
    if player == 1:
        return 2
    else:
        return 1


#assinala (ou desassinala tipo=0) uma quadricula x,y
def assinala_quad(x, y, atip):
    if moves.player == 1:
        pygame.draw.ellipse(atip, (187, 150, 225), (x*sq+5, y*sq+5, 4, 4))
        pygame.draw.ellipse(atip, (187, 150, 225), (x*sq+sq-5, y*sq+5, 4, 4))
        pygame.draw.ellipse(atip, (187, 150, 225), (x*sq+5 ,y*sq+sq-5, 4, 4))
        pygame.draw.ellipse(atip, (187, 150, 225), (x*sq+sq-5, y*sq+sq-5, 4, 4))
    
    else :
        pygame.draw.ellipse(atip, (160, 213, 180), (x*sq+5, y*sq+5, 4, 4))
        pygame.draw.ellipse(atip, (160, 213, 180), (x*sq+sq-5, y*sq+5, 4, 4))
        pygame.draw.ellipse(atip, (160, 213, 180), (x*sq+5 ,y*sq+sq-5, 4, 4))
        pygame.draw.ellipse(atip, (160, 213, 180), (x*sq+sq-5, y*sq+sq-5, 4, 4))


#Mostra o tabuleiro em modo grafico
def mostra_tabul(atip, tab):
    for i in range(N): 
        for j in range(N): 
            pygame.draw.rect(atip, (250,250,250), pygame.Rect(j*sq+1,i*sq+1,j*sq+sq-1,i*sq+sq-1)) #quadrado branco

            if tab[i][j] == 8:
                pygame.draw.rect(atip, (50,50,50), pygame.Rect(j*sq+1,i*sq+1,j*sq+sq-1,i*sq+sq-1)) #quadrado preto
        	
            if tab[i][j] == 1:
                pygame.draw.ellipse(atip, (187, 150, 225), (j*sq+sq/2,i*sq+sq/2,sq/2-7,sq/2-7))
            elif tab[i][j] == 2:
                 pygame.draw.ellipse(atip, (160, 213, 180), (j*sq+sq/2,i*sq+sq/2,sq/2-7,sq/2-7))

		
#le o jogo do ficheiro, não atualiza o jogador nem o numero da jogada
def le_jogo(fich):
    f = open(fich, "r")

    if os.stat(fich).st_size == 0:
        print("Impossivel ler o ficheiro %s") %fich   #cheka se o fich esta vazio ou não

    a = f.readline().split()  #not sure if this works, but i m separating everything 
    N = int(a[0])                  # and expecting N to the the frist thing on the list xc

    # a seria uma cena do genro = [N, 0000, 8880, 0000] , para um tabuleiro de 4x4

    a = a[1::] # i removed the 1st thing which again i assume its N so that the positions are alright now

    for i in range(N): 
        for j in range(N):		# these for do not work, index out of range, sme thing for the next function, the rest is alright
            tab[i][j] = a[i][j]		# thei re imcomplete tho
	
   
#Grava o estado do jogo num ficheiro
def garva_jogo():
    f = open(fich, "r")

    if os.stat(fich).st_size == 0:
        print("Impossivel ler o ficheiro %s") %fich   #cheka se o fich esta vazio ou não

    a = f.readline().split() 
    N = int(a[0])            
    a = a[1::]

    for i in range(N):
        for j in range(N): 
            
