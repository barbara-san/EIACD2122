import time
import os
from turtle import delay
import pygame

from pynput import mouse

from tkinter import *
import numpy as np

pygame.init()

SIZE = 600
window = Tk()
canvas = Canvas(window, width=SIZE, height=SIZE)

# estado do tabuleiro


class tabuleiro:
    N = 8  # tamanho do tabuleiro
    sq = (SIZE / N)  # tamanho da celula
    tab = []
    tabcopia = []
    Ntabs = 6  # numero de ficheiros de tabuleiros
    nMovs = 0


fich = "fich.txt"  # nome do ficheiro com os mapas


class moves:
    xi = 0
    yi = 0
    xf = 0
    yf = 0
    player = 0
    tipo = 0
    winner = 0


def copia():
    for i in range(tabuleiro.N):
        for j in range(tabuleiro.N):
            tabuleiro.tabcopia[j][i] = tabuleiro.tab[j][i]


def restaurar():
    for i in range(tabuleiro.N):
        for j in range(tabuleiro.N):
            tabuleiro.tab[i][j] = tabuleiro.tabcopia[j][i]


# dado o jogador atual, retorna o outro jogador
def otherplayer():
    if moves.player == 1:
        return 2
    else:
        return 1


# assinala (ou desassinala tipo=0) uma quadricula x,y
def assinala_quad(x, y, canvas):
    if moves.player == 1:
        pygame.draw.ellipse(canvas, (187, 150, 225),
                            (x*tabuleiro.sq+5, y*tabuleiro.sq+5, 4, 4))
        pygame.draw.ellipse(
            canvas, (187, 150, 225), (x*tabuleiro.sq+tabuleiro.sq-5, y*tabuleiro.sq+5, 4, 4))
        pygame.draw.ellipse(
            canvas, (187, 150, 225), (x*tabuleiro.sq+5, y*tabuleiro.sq+tabuleiro.sq-5, 4, 4))
        pygame.draw.ellipse(canvas, (187, 150, 225),
                            (x*tabuleiro.sq+tabuleiro.sqq-5, y*tabuleiro.sq+tabuleiro.sq-5, 4, 4))

    else:
        pygame.draw.ellipse(canvas, (160, 213, 180),
                            (x*tabuleiro.sq+5, y*tabuleiro.sqq+5, 4, 4))
        pygame.draw.ellipse(
            canvas, (160, 213, 180), (x*tabuleiro.sq+tabuleiro.sqq-5, y*tabuleiro.sq+5, 4, 4))
        pygame.draw.ellipse(
            canvas, (160, 213, 180), (x*tabuleiro.sq+5, y*tabuleiro.sq+tabuleiro.sq-5, 4, 4))
        pygame.draw.ellipse(canvas, (160, 213, 180),
                            (x*tabuleiro.sq+tabuleiro.sq-5, y*tabuleiro.sq+tabuleiro.sq-5, 4, 4))


# Mostra o tabuleiro em modo grafico
def mostra_tabul():
    for i in range(tabuleiro.N):
        for j in range(tabuleiro.N):
            pygame.draw.rect(canvas, (250, 250, 250), pygame.Rect(
                j*tabuleiro.sq+1, i*tabuleiro.sq+1, j*tabuleiro.sq+tabuleiro.sq-1, i*tabuleiro.sq+tabuleiro.sq-1))  # quadrado branco

            if tabuleiro.tab[i][j] == 8:
                pygame.draw.rect(canvas, (50, 50, 50), pygame.Rect(
                    j*tabuleiro.sq+1, i*tabuleiro.sq+1, j*tabuleiro.sq+tabuleiro.sq-1, i*tabuleiro.sq+tabuleiro.sq-1))  # quadrado preto

            if tabuleiro.tab[i][j] == 1:
                pygame.draw.ellipse(canvas, (187, 150, 225),
                                    (j*tabuleiro.sq+tabuleiro.sq/2, i*tabuleiro.sq+tabuleiro.sq/2, tabuleiro.sq/2-7, tabuleiro.sq/2-7))
            elif tabuleiro.tab[i][j] == 2:
                pygame.draw.ellipse(canvas, (160, 213, 180),
                                    (j*tabuleiro.sq+tabuleiro.sq/2, i*tabuleiro.sq+tabuleiro.sq/2, tabuleiro.sq/2-7, tabuleiro.sq/2-7))


# lê o jogo do ficheiro, não atualiza o jogador nem o numero da jogada
def read_game(fich):
    if os.stat(fich).st_size == 0:
        print("Impossivel ler o ficheiro", fich)
    else:
        f = open(fich, "r")
        tabuleiro.N = int(f.readline())
        tabuleiro.sq = SIZE / tabuleiro.N
        tabul = []

        for i in range(tabuleiro.N):
            tabul.append(list(map(int, f.readline().split())))
        f.close()

    tabuleiro.tab = tabul


# Grava o estado do jogo num ficheiro
'''def grava_jogo():
     f = open(fich, "r")
    if os.stat(fich).st_size == 0:
        # verifica se o ficheiro esta vazio ou não
        print("Impossivel ler o ficheiro %s") %fich
    a = f.readline().split()
    N = int(a[0])
    a = a[1::]
    for i in range(N):
        for j in range(N): '''

# Inicializa o Tabuleiro lendo sucessivamente os varios tabs de ficheiros


def inicia_tabu():
    print("Tabuleiros:")
    print("1) 20x20")
    print("2) 8x8")
    print("3) 16x16")
    print("4) 4x4")
    print("5) 7x7")
    print("6) 7x7")
    numtab = input()
    fich = "tab" + numtab + ".txt"
    read_game(fich)
    mostra_tabul()

    '''for i in range(1,7):
        if i > 6:
            i = 1
        fich = "tab"+ i + ".txt"
        read_game(fich)
        mostra_tabul()
        delay(800)'''


# Pede ao utlizador que escolha um dos 4 modos de jogo possiveis:
# 1-Hum/Hum 2-Hum/PC 3-PC/Hum 4-PC/PC
def tipo_jogo():
    print("Jogo de Attax")
    print("Escolah o modo de jogo:")
    print("1-Hum/Hum")
    print("2-Hum/AI")
    print("3-AI/AI")
    modo = int(input())
    return modo


# Finaliza o jogo indicando quem venceu ou se foi empate
def finaliza():
    if moves.winner == 1:
        text = "Venceu o jogador 1!"
    elif moves.winner == 2:
        text = "Venceu o jogador 2!"
    else:
        text = "Foi empate!"
    canvas.create_text(SIZE/2, SIZE/2, font="cmr 30 bold",
                       fill="black", text=text)


# Indica se (x,y) esta dentro do tabuleiro
def dentro(x, y):
    if (x >= 0 and x <= (tabuleiro.N - 1) and y >= 0 and y <= (tabuleiro.N - 1)):
        return True
    else:
        return False

# Indica se mov se verifica entre duas coordenadas adjacentes a 1 ou 2 de distancia


def adjacente(dist):
    if(abs(moves.xi - moves.xf) == dist and abs(moves.yi-moves.yf) <= dist) or (abs(moves.yi - moves.yf) == dist and abs(moves.xi - moves.xf) <= dist):
        return True
    else:
        return False

# indica se mov e um movimento valido e qual o seu tipo


def movimento_valido():
    if(not(dentro(moves.xi, moves.yi)) or not(dentro(moves.xf, moves.yf))):
        return False  # fora do tabuleiro

    if tabuleiro.tab[moves.yi][moves.xi] == moves.player and tabuleiro.tab[moves.yf][moves.xf] == 0 and adjacente(1):
        moves.tipo = 0
        return True

    if tabuleiro.tab[moves.yi][moves.xi] == moves.player and tabuleiro.tab[moves.yf][moves.xf] == 0 and adjacente(2):
        moves.tipo = 1
        return True

    return False


def multiplica():
    for x in range(1):
        for y in range(1):
            if tabuleiro.tab[moves.yf + y][moves.xf + x] == otherplayer(moves.player):
                tabuleiro.tab[moves.yf + y][moves.xf + x] = moves.player


# executa o movimento moves do tipo tipo
def executa_moves():
    tabuleiro.tab[moves.yf][moves.xf] = moves.player
    
    if moves.tipo == 1:
        tabuleiro.tab[moves.yi][moves.xi] = 0
        multiplica()


def conta_pecas(num):
    cp = 0
    for i in range(tabuleiro.N):
        for j in range(tabuleiro.N):
            if tabuleiro.tab[i][j] == num:
                cp += 1
    return cp


def avalia():
    return (conta_pecas(moves.player) - (conta_pecas(otherplayer(moves.player))))


# movimento do Computador - Joga Aleatotio
def jogada_PC():
    moves.xi = 0
    moves.yi = 0
    moves.xf = 0
    moves.yf = 0
    moves.player = 0
    moves.tipo = 0

    bestav = - 1000
    for yi in range(tabuleiro.N):
  	    for xi in range(tabuleiro.N):
  	        for yf in range(tabuleiro.N):
  		        for xf in range(tabuleiro.N):
  			        moves.yi = yi, moves.xi = xi, moves.yf = yf, moves.xf = xf
                    if movimento_valido():
                        copia()
                        executa_moves()
                        av = avalia(moves.player)
                        if av >= bestav:
                            bestav = av
                            bestmov = moves
                            print("%d %d -> %d %d (%d): %d", moves.yi, moves.xi, moves.yf, moves.xf, moves.tipo, av)
                            restaurar()
    executa_moves(bestmov)


#determina todas as jogadas validas de um jogador 
def jogadas_validas():
    



