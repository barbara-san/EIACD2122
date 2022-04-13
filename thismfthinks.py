import random


gameoverwin = 100000


def random (validmoveslist):
    return validmoveslist[random.randint(0, len(validmoveslist) - 1)]

def greedy(gamestate, validmoveslist):
    whoplaying = 1 if player1turn else -1
    maxscore = -gameoverwin
    bestmove = None
    for move1 in validmoveslist:
        makeMove(move1)                #here
        if gs.checkmate:               #here - game over first wins
            score = gameoverwin
        elif validmoveslist == []:             #here -  empate/ sem movimentos possiveis
            score = 0
        else:
            score = whoplaying * boardscore(board)      #here
        if score > maxscore:
            maxscore = score
            bestmove = move1
        undoMove()                     #here
    return bestmove

def minimax(gamestate, validmoveslist): # up to 2 moves, not recursive
    whoplaying = 1 if player1turn else -1
    opponentminmaxscore = gameoverwin
    best1move = None
    random.shuffle(validmoveslist)

    for moveplayer1 in validmoveslist:
        makeMove(moveplayer1)               #here
        opponentmoves = getvalidmoves()     #here
        if validmoveslist == []:
        opponentmaxscore = 0
        elif checkmate:
            opponentmaxscore = -gameoverwin
        else:
            opponentmaxscore = -gameoverwin
            for moveplayer2 in opponentmoves:
                makeMove(moveplayer2)
                getvalidmoves()
                if checkmate:               #here - game over first wins
                    score = gameoverwin
                elif validmoveslist == []:             #here -  empate/ sem movimentos possiveis
                    score = 0
                else:
                    score = -whoplaying * boardscore(board)      #here
                if score > opponentmaxscore:
                    opponentmaxscore = score
                undoMove()
        if opponentmaxscore < opponentminmaxscore:
            opponentminmaxscore = opponentmaxscore
            best1move = moveplayer1
        undoMove()                     #here
    return best1move

'''
def betterminimax(gamestate, validmoveslist):
    global nextMove
    nextMove = None
    betterminimax2(gamestate, validmoveslist, depth, player)
    return nextMove

def betterminimax2(gamestate, validmoveslist, depth, player): #recursive
    global nestMove
    if depth == 0:
        return boardscore(board)
'''

def boardscore(board):
    score = 0
    for row in board:
        for line in board:
            if line == 1:
                score += 1
            elif line == 2:
                score-=1
