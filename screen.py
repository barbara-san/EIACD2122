from sys import exit
import pygame as py
import os

'''LOADS INITIAL GAME STATE ====================================================='''

def get_tab(fich):
# reads a file and updates tab, doesnt change anything visually 
    if os.stat(fich).st_size == 0:
        print("File impossible to read", fich)

    else:
        f = open(fich, "r")
        n = int(f.readline())
        tab = []

        for i in range(n):
            tab.append(list(map(int, f.readline().split())))
        f.close()
        
    return n, tab

def choose_tab():
    print("Boards:")
    print("1) 20x20")
    print("2) 8x8")
    print("3) 16x16")
    print("4) 4x4")
    print("5) 7x7")
    print("6) 7x7")
    numtab = input()
    fich = "tab" + numtab + ".txt"

    n, tab = get_tab(fich)

    return n, tab


'''GAPHIC PART==================================================================='''

# used colours
white = (250, 250, 250)  # 0
colour1 = (187, 150, 225)  # 1
colour2 = (104, 213, 163)  # 2
backg1 = (224, 212, 236)  # 3
backg2 = (200, 229, 215)  # 4
black = (0, 0, 0)  # 8
grey = (96, 96, 96)

def show_tab(screen, n):
    # draws tab frame
    py.draw.line(screen, black, (0, 0), (SIZE, 0), 2)
    py.draw.line(screen, black, (0, 0), (0, SIZE), 2)
    py.draw.line(screen, black, (0, 798), (SIZE, 798), 2)
    py.draw.line(screen, black, (798, 0), (798, SIZE), 2)

    # draws lines and columns
    for i in range(1, n):
        py.draw.line(screen, black, (SIZE*i/n, 0), (SIZE*i/n, SIZE), 2)
        py.draw.line(screen, black, (0, SIZE*i/n), (SIZE, SIZE*i/n), 2)


def draw_pieces(screen, tab, n):
    for i in range(n):
        for j in range(n):
            if tab[i][j] == 1:
                # draws pieces from player 1
                py.draw.circle(screen, colour1, ((SIZE*i/n) + SIZE /
                               (2*n), (SIZE*j/n) + SIZE / (2*n)), SIZE/(3*n))

            elif tab[i][j] == 2:
                # draws pieces from player 2
                py.draw.circle(screen, colour2, ((SIZE*i/n) + SIZE /
                               (2*n), (SIZE*j/n) + SIZE / (2*n)), SIZE/(3*n))

            elif tab[i][j] == 8:
                # draws walls
                py.draw.rect(screen, grey, (SIZE*i/n +2, SIZE *
                             j/n +2, SIZE/n -2, SIZE/n -2))


def show_selected(screen, tab, n):
    # highlights the possitions for possible next moves
    for i in range(n):
        for j in range(n):
            if tab[i][j] == 3:
                py.draw.rect(screen, backg1, (SIZE*i/n + 2,
                             SIZE * j/n + 2, SIZE/n - 2, SIZE/n - 2))
            elif tab[i][j] == 4:
                py.draw.rect(screen, backg2, (SIZE*i/n + 2,
                             SIZE * j/n, SIZE/n - 2, SIZE/n + 2))


def draws_gameState(screen, tab ,n):
    show_tab(screen, n)
    draw_pieces(screen, tab, n)


'''ENGINE ========================================================================'''

# keeps track of the moves state 
class Move:
    def __init__(self, startSq, endSq, tab):
        self.startRow = startSq[1]
        self.startCol = startSq[0]
        self.endRow = endSq[1]
        self.endCol = endSq[0]

        self.pieceMoved = tab[int(self.startRow)][int(self.startCol)]
        self.type = 1 #moveType() # 1(copy) or 2(jump)
        self.player = 1


    def moveType():
        pass


def otherPlayer(move):
    if move.player == 1:
        return 2
    elif move.player == 2:
        return 1
 

def makeMove(move):       
# if moveType == jump, then deletes piece from initial state and puts it in new position 
# also switches player
    if move.type == 2:
        if tab[int(move.startRow)][int(move.startCol)] == 1:
            tab[int(move.endRow)][int(move.endCol)] = 1
        elif tab[int(move.startRow)][int(move.startCol)] == 2:
            tab[int(move.endRow)][int(move.endCol)] = 2

        tab[int(move.startRow)][int(move.startCol)] = 0
    
    elif move.type == 1:
        if tab[int(move.startRow)][int(move.startCol)] == 1:
            tab[int(move.endRow)][int(move.endCol)] = 1
        elif tab[int(move.startRow)][int(move.startCol)] == 2:
            tab[int(move.endRow)][int(move.endCol)] = 2

    move.player = otherPlayer(move)

     
'''MAIN =========================================================================='''
   
# size of the screen and creating a white canvas
SIZE = 600

screen = py.display.set_mode((SIZE, SIZE))


n, tab = choose_tab()
SQ_SIZE = SIZE / n

running = True

sq_selected = () # no square is selected initialy, keep strack of the last click of teh user 
playerClicks = [] # keeps track of player clicks ex:[(1,2),(2,2)]

while running:
    events = py.event.get()
    screen.fill(white)
    draws_gameState(screen, tab, n)
    show_selected(screen, tab, n)

    for event in events:
        if event.type == py.QUIT:
            running = False
            
        elif event.type == py.MOUSEBUTTONDOWN:
            location = py.mouse.get_pos() # (x,y) location of the mouse 
            col = location[0]//SQ_SIZE
            row = location[1]//SQ_SIZE

            if sq_selected == (row, col): # the user clicks the same square twice
                sq_selected = ()
                playerClicks = []
            else:
                sq_selected = (row, col) 
                playerClicks.append(sq_selected) # append both 1st and 2nd clicks

            if len(playerClicks) == 2:
                move = Move(playerClicks[0], playerClicks[1], tab)
                print(tab)
                makeMove(move)
                sq_selected = () #reset user clicks 
                playerClicks = []
            

    py.display.update()
