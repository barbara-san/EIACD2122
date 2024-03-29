import sys
import pygame as py
import numpy as np
import random as rd
import copy as cp

'''CHOOSE GAME MODE ============================================================='''

def gameMode(): 
# askes the user for the game mode they want to play

    print("Choose a game mode:")
    print("1. Human VS Human")
    print("2. Human VS AI")
    print("3. AI VS AI")
    
    mode = int(input())
    
    if mode == 1:
        gamemode = [1, 2]
        return gamemode

    elif mode == 2:
        print("Choose the AI difficulty:")
        print("1. Easy")                                # Easy random moves from the AI
        print("2. Medium")                              # Medium moves made using a greedy algorithm
        print("3. Hard")                                # Hard moves made using a MiniMax algorithm
        dif = int(input()) + 5
        gamemode = [1, dif]
        return gamemode
        

    elif mode == 3:
        print("Choose the player 1 difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        dif1 = int(input()) + 5
        print("Choose the player 2 difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        dif2 = int(input()) + 5 
        gamemode = [dif1, dif2]
        return gamemode 

# Each of these functions will return information about each player, whether it is a Human player, returning 4
# or an AI player, returning their difficulty (1 , 2 or 3)


'''LOADS INITIAL GAME STATE ====================================================='''

def get_tab(fich):
# reads a file and updates the board, doesnt change anything visually

    f = open(fich, "r")
    n = int(f.readline())
    tab = []
    for i in range(n):
        tab.append(list(map(int, f.readline().split())))
    f.close()

    return n, tab


def choose_tab():
# Asks user to choose a board to play

    print("Choose the board you wanna play:")
    print("1. 20x20")
    print("2. 8x8")
    print("3. 16x16")
    print("4. 4x4")
    print("5. 7x7")
    print("6. 7x7")
    numtab = input()
    fich = "tab" + numtab + ".txt"

    n, tab = get_tab(fich)

    return n, tab        # returns the board and their length  


'''GRAPHIC PART==================================================================='''

# used colours
white = (250, 250, 250)      # useed as the base colour for our board
black = (0, 0, 0)            # used to draw lines to deffine columns and rows on the board
colour1 = (187, 150, 225)    # 1, used as the colour for player 1
colour2 = (104, 213, 163)    # 2, used as the colour for player 2
backg1 = (224, 212, 236)     # 3, used to highlight possible moves for player 1
backg2 = (200, 229, 215)     # 4, used to highlight possible moves for player 2
grey = (96, 96, 96)          # 8, used to define walls 


# draws the board
def show_tab(screen, n):
    # draws the board frame
    py.draw.line(screen, black, (0, 0), (SIZE, 0), 2)
    py.draw.line(screen, black, (0, 0), (0, SIZE), 2)
    py.draw.line(screen, black, (0, 798), (SIZE, 798), 2)
    py.draw.line(screen, black, (798, 0), (798, SIZE), 2)

    # draws lines, creating rows and columns on the board
    for i in range(1, n):
        py.draw.line(screen, black, (SIZE*i/n, 0), (SIZE*i/n, SIZE), 2)
        py.draw.line(screen, black, (0, SIZE*i/n), (SIZE, SIZE*i/n), 2)


# draws pieces for each player and walls
def draw_pieces(screen, tab, n):
    for i in range(n):
        for j in range(n):
            if tab[i][j] == 1:
                # draws pieces for player 1
                py.draw.circle(screen, colour1, ((SIZE*i/n) + SIZE /
                               (2*n), (SIZE*j/n) + SIZE / (2*n)), SIZE/(3*n))

            elif tab[i][j] == 2:
                # draws pieces for player 2
                py.draw.circle(screen, colour2, ((SIZE*i/n) + SIZE /
                               (2*n), (SIZE*j/n) + SIZE / (2*n)), SIZE/(3*n))

            elif tab[i][j] == 8:
                # draws walls
                py.draw.rect(screen, grey, (SIZE*i/n + 2, SIZE *
                             j/n + 2, SIZE/n - 2, SIZE/n - 2))


# highlights possible next moves
def show_selected(screen, tab, n):
    for i in range(n):
        for j in range(n):
            if tab[i][j] == 3:
                py.draw.rect(screen, backg1, (SIZE*i/n + 2,
                             SIZE * j/n + 2, SIZE/n - 2, SIZE/n - 2))
            elif tab[i][j] == 4:
                py.draw.rect(screen, backg2, (SIZE*i/n + 2,
                             SIZE * j/n + 2, SIZE/n - 2, SIZE/n - 2))


def draws_gameState(screen, tab, n):
    show_tab(screen, n)
    draw_pieces(screen, tab, n)


'''ENGINE ========================================================================'''

moveLog = []
player = 1      # fist player to move is always player 1 

end = -1        # this variable is used to store the game state: 
                # -1 => game still in process
                # 0 => game ends in a tie
                # 1 => game ends with player 1 winning 
                # 2 => game ends with player 2 winning


# keeps track of the moves state
class Move:
    def __init__(self, startSq, endSq, validMoves, tab):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = tab[int(self.startRow)][int(self.startCol)]
        self.moveLog = []
        self.type = None
        for i in range(len(validMoves)):
            if self.endRow == validMoves[i][0][0] and self.endCol == validMoves[i][0][1]:
                self.type = validMoves[i][1] # moveType() # 1(copy) or 2(jump)


# returns next player to move
def otherPlayer():
    if player  == 1:
        return 2
    elif player  == 2:
        return 1


# makes one of the two possible moves, jump(2) and copy(1)
def makeMove():
    if move.type == 2:
        if player == 1:
            tab[int(move.endRow)][int(move.endCol)] = 1
        elif player == 2:
            tab[int(move.endRow)][int(move.endCol)] = 2
        tab[int(move.startRow)][int(move.startCol)] = 0

    elif move.type == 1:
        if player == 1:
            tab[int(move.endRow)][int(move.endCol)] = 1
        elif player == 2:
            tab[int(move.endRow)][int(move.endCol)] = 2


# when a player is out of moves, this function skips their turn until a possible move is available
def skip(player,n):
    for i in range(n):
        for j in range(n):
            piece = tab[i][j]
            board = np.array(tab)
            if piece == player:
                if len(get_validMoves([(i,j)],player)) > 0 or np.count_nonzero(board == player+2) >0:
                    return False
    return True


# returns a list of all the possible moves for the piece selected 
def get_validMoves(playerClicks,player):
    # list of all possible moves in the board:
    possibleMoves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (2, 2), (-1, 0), (-2, 0), (0, -1), (0, -2), (-1, -1), (-2, -2), (-1, 1), (1, -1), (-2, 2), (2, -2)]
    validMoves = []
    initial = (int(playerClicks[0][0]),int(playerClicks[0][1]))

    for mov in possibleMoves:
        play = (initial[0] + mov[0], initial[1] + mov[1])
        if not(play[0] < 0 or play[0] > (n-1) or play[1] < 0 or play[1] > (n-1)) and tab[initial[0]][initial[1]]==player:
            if tab[int(play[0])][int(play[1])] == 0:
                if 1 in mov or -1 in mov:
                    validMoves.append((play,1))
                elif 2 in mov or -2 in mov:
                    validMoves.append((play,2))
    return validMoves


# makes the changes on the board to highlight the possible moves 
def showPossibleMoves(validMoves,player):
    if player  == 1:
        for i in range(len(validMoves)):
            tab[validMoves[i][0][0]][validMoves[i][0][1]] = 3
            show_selected(screen, tab, n)
    else:
        for i in range(len(validMoves)):
            tab[validMoves[i][0][0]][validMoves[i][0][1]] = 4
            show_selected(screen, tab, n)


# returns a list with all the possible moves for the AI can analyze
def getAllPossibleMoves(player, tab):
    possibleMoves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (2, 2), (-1, 0), (-2, 0), (0, -1), (0, -2), (-1, -1), (-2, -2), (-1, 1), (1, -1), (-2, 2), (2, -2)]
    allPieces = []
    validMoves = []
    for row in range(len(tab)):
        for square in range(len(tab)):
            if tab[row][square] == player:
                allPieces.append((row, square))
    for mov in possibleMoves:
        for squar in range(len(allPieces)):
            play = (allPieces[squar][0] + mov[0], allPieces[squar][1] + mov[1])
            if not(play[0] < 0 or play[0] > (n-1) or play[1] < 0 or play[1] > (n-1)) and tab[allPieces[squar][0]][allPieces[squar][1]]==player:
                if tab[int(play[0])][int(play[1])] == 0:
                    if 1 in mov or -1 in mov:
                        validMoves.append((allPieces[squar],play,1))
                    elif 2 in mov or -2 in mov:
                        validMoves.append((allPieces[squar],play,2))
    return validMoves


# when a new piece is placed next to another, the old piece takes the colour of the new one
def next_to():
    adj = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1], [1,-1], [-1,1]]
    for i in range(len(adj)):
        x = int(move.endRow) + int(adj[i][0])
        y = int(move.endCol) + int(adj[i][1])
        
        if x >= 0 and x < n and y >= 0 and y < n:

            if player  == 1:
                if tab[x][y] == 2:
                    tab[x][y] = 1
            elif player  == 2:
                if tab[x][y] == 1:
                    tab[x][y] = 2


'''OTHER_DATA ===================================================================='''

# counts each players pieces on the board 
def count(tab):
    nPURPLE = 0
    nGREEN = 0
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[i][j] == 1:
                nPURPLE += 1
            elif tab[i][j] == 2:
                nGREEN += 1
    count = [nPURPLE, nGREEN]
    return count


# checks the game state: still going? finished? who won? was it a tie?
def checkEnd(tab, player):
    board = np.array(tab)
    if np.count_nonzero(board == 3-player) == 0:
        return player 

    if np.count_nonzero(board == 0) != 0:
        return -1
    else:
        scores = count(tab)
        if scores[0] > scores[1]:
            return 1
        elif scores[0] < scores[1]:
            return 2
        else:
            return 0

'''END_GAME ======================================================================'''

# prints the winner of the game or if it was a tie
def end_game(end):
    if end == 0:
        print("It's a tie!")
    elif end == 1:
        print("Purple player won!")
    elif end == 2:
        print("Green player won!")

'''AI ======================================================================'''

# returns a random move
def random(validMovesAI):
    return validMovesAI[rd.randint(0, len(validMovesAI) - 1)]

def boardscore():
    countt = count(tab)
    return countt[0] - countt[1]


# returns a score of the board; positive = better for player 1; negative = better for second player
'''def boardscore(tab):
    nPURPLE = 0
    nGREEN = 0
    for i in range(n):
        for j in range(n):
            if (len(tab) - (len(tab)/4 + 1- len(tab)%4) >= i >= len(tab)/4 + 1- len(tab)%4) and (len(tab) - (len(tab)/4 + 1- len(tab)%4) >= i >= len(tab)/4 + 1- len(tab)%4):
                if tab[i][j] == 1:
                    nPURPLE += 2
                elif tab[i][j] == 2:
                    nGREEN += 2
            else:
                if tab[i][j] == 1:
                    nPURPLE += 1
                elif tab[i][j] == 2:
                    nGREEN += 1       
    return nPURPLE - nGREEN # based on the amount of pieces of each player, the ones closer to the center value more


def heuristics(move, player):
    if player == 1:
        a = 2
    elif player == 2:
        a = 1
    count = 0
    around = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]
    initial = (move[1][0], move[1][1])

    if move[2] == 1:    # if the move type is copy
        count += 1    

    for piece in around:    # counts the amount of pieces of the opponent around the destination
        piecenear = (initial[0] + piece[0], initial[1] + piece[1])
        if not(piecenear[0] < 0 or piecenear[0] > (n-1) or piecenear[1] < 0 or piecenear[1] > (n-1)) and tab[initial[0]][initial[1]]==player and tab[piecenear[0]][piecenear[1]]==a:
            count += 1     
    return count
    '''

def greedy(tab, validMovesAI, gamemode, player):
    if gamemode[0] == 7:
        whoplaying = 1 
    elif gamemode[1] == 7:
        whoplaying = -1
    maxscore = -10000
    bestmove = None
    copy = cp.deepcopy(tab)
    for moveAI in validMovesAI:
        AImove = moveAI
        AIpiece = [AImove[0]]
        validMoves = get_validMoves(AIpiece, player)
        move = Move(AImove[0], AImove[1], validMoves, tab)
        makeMove()
        a = cp.deepcopy(count(tab))
        tab = copy
        if (checkEnd(tab, player) == 1 and whoplaying == 1):
            score = 10000
        elif validMoves == [] or checkEnd(tab, player) == 0:
            score = 0
        else:
            score = boardscore() * whoplaying #+ heuristics(AImove, player)
        if score > maxscore:
            maxscore = score
            bestmove = AImove
    print(a)
    return bestmove

def findBestMove(tab, validMovesAI, player, DEPTH):
    global next_move
    next_move = None
    if player == 1:
        whoplaying = 1 
    elif player == 2:
        whoplaying = -1
    #random.Shuffle(validMovesAI)
    minimaxAlphaBeta(tab, validMovesAI, player, 5, -10000, 10000, whoplaying, DEPTH)
    return next_move

def minimaxAlphaBeta(tab, validMovesAI, player, depth, alpha, beta, whoplaying, DEPTH):
    global next_move
    if depth == 0:
        return whoplaying * (boardscore(tab) + heuristics(AImove))
    max_score = -10000
    copy = cp.deepcopy(tab)
    for moveAI in validMovesAI:
        AImove = moveAI
        validAI = [AImove[0]]
        validMoves = get_validMoves(validAI, player)
        move = Move(AImove[0], AImove[1], validMoves, tab)
        makeMove()
        next_moves = getAllPossibleMoves(player, tab)
        score = -minimaxAlphaBeta(tab, next_moves, player, depth - 1, -beta, -alpha, -whoplaying, DEPTH)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = AImove
        tab = copy
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

'''MAIN =========================================================================='''

gamemode = gameMode() # returns a list end [1, 6]: 1 = player1_human, 2 = player2_human, 6 = random, 7 = greedy, 8 = minimax  

# size of the screen and creating a white canvas
n, tab = choose_tab()
SIZE = 800
SQ_SIZE = SIZE / n
MOVECOUNT = 0
moveLog = []
screen = py.display.set_mode((SIZE, SIZE))

running = True
player = 1
sq_selected = ()  # no square is selected initially, keeps track of the last click of the user
playerClicks = []  # keeps track of player clicks ex:[(1,2),(2,2)]
clickState = False
if len(tab) <= 8:
    DEPTH = 4
else:
    DEPTH = 3

while running:
    events = py.event.get()
    screen.fill(white)
    draws_gameState(screen, tab, n)
    show_selected(screen, tab, n)

    for event in events:
        if event.type == py.QUIT:
            sys.exit()

        if not(skip(player,n)):

            if gamemode[player -1] == player: # meaning, both players are human

                if (event.type == py.MOUSEBUTTONDOWN) and (clickState == False):
                    location = py.mouse.get_pos()  # (x,y) location of the mouse
                    clickState = True                   
                    row = location[0]//SQ_SIZE
                    col = location[1]//SQ_SIZE
                    sq_selected = (row,col)
                    playerClicks.append(sq_selected)

                elif (event.type == py.MOUSEBUTTONDOWN) and (clickState == True):
                    location = py.mouse.get_pos()
                    clickState = False
                    row = int(location[0]//SQ_SIZE)
                    col = int(location[1]//SQ_SIZE)

                    if sq_selected == (row, col):  # the user clicks the same square twice
                        if tab[row][col] == 3-player or tab[row][col] != player + 2:  
                            sq_selected = ()
                            playerClicks = []
                            for i in range(n):
                                for j in range(n):
                                    if tab[i][j] == 3 or tab[i][j] == 4:
                                        tab[i][j] = 0

                    elif tab[row][col] == player +2 :
                        sq_selected = (row, col)
                        playerClicks.append(sq_selected)  # append both 1st and 2nd clicks

                if len(playerClicks) == 1:
                    possibilities = get_validMoves(playerClicks,player)
                    showPossibleMoves(possibilities,player)

                elif len(playerClicks) == 2:
                    for i in range(n):
                        for j in range(n):
                            if tab[i][j] == 3 or tab[i][j] == 4:
                                tab[i][j] = 0
                    possibilities = get_validMoves(playerClicks,player)
                    move = Move(playerClicks[0], playerClicks[1], possibilities, tab)
                    MOVECOUNT += 1
                    
                    makeMove()
                    next_to()
                    end = checkEnd(tab,player)
                    end_game(end)

                    sq_selected = ()  # reset user clicks
                    playerClicks = []
                    player  = otherPlayer()
                    
            else: # its AI turn 
                if gamemode[player -1] == 6: # random moves
                    validMovesAI = getAllPossibleMoves(player, tab)
                    AImove = random(validMovesAI)
                    AIpiece = [AImove[0]]
                    validMoves = get_validMoves(AIpiece, player)
                    move = Move(AImove[0], AImove[1], validMoves, tab)
                    MOVECOUNT += 1
                    makeMove()
                    next_to()
                    end = checkEnd(tab,player)
                    end_game(end)
                    player  = otherPlayer()           # ADD DELAY AFTER PLAY FOR THE AI VS AI MODE
                    
                elif gamemode[player -1] == 7:
                    validMovesAI = getAllPossibleMoves(player, tab)
                    copytab = cp.deepcopy(tab)
                    AImove = greedy(tab, validMovesAI, gamemode, player)
                    tab = copytab
                    AIpiece = [AImove[0]]
                    validMoves = get_validMoves(AIpiece, player)
                    move = Move(AImove[0], AImove[1], validMoves, tab)
                    MOVECOUNT += 1
                    makeMove()
                    next_to()
                    end = checkEnd(tab,player)
                    end_game(end)
                    player  = otherPlayer()
                    
                elif gamemode[player -1] == 8:
                    validMovesAI = getAllPossibleMoves(player, tab)
                    copytab = cp.deepcopy(tab)
                    AImove = findBestMove(tab, validMovesAI, player, DEPTH)
                    tab = copytab
                    AIpiece = [AImove[0]]
                    validMoves = get_validMoves(AIpiece, player)
                    move = Move(AImove[0], AImove[1], validMoves, tab)
                    MOVECOUNT += 1
                    makeMove()
                    next_to()
                    end = checkEnd(tab,player)
                    end_game(end)
                    player  = otherPlayer()
             
        else:
            player = otherPlayer()
                  
    py.display.update()


    if end != -1:
        running = False   #if you dont want it to close right after someone wins, just remove this if
