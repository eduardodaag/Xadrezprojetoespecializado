#jogo será rodado aqui

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))

"""

Main driver, user inputs and updating

"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable when move made
    animate = False #flag variable for when should animate a move
    loadImages()
    running = True
    sqSelected = () #no square selected, keep track of the last click of the user
    playerClicks = [] #keep track of the player ckicks, dois tuples
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            ##mouse selecao
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #localizacao do mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): ##user selected same square:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) ##append clique e segundo clique
                    if len(playerClicks) == 2: #depois do 2o clique
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True
                                animate = True
                                sqSelected = () ##reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: ##desfaz se z é pressionado
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves=gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")

        elif gs.staleMate:
            drawText(screen, "Draw")

        clock.tick(MAX_FPS)
        p.display.flip()

"""
highlighted square selected and moves for piece selected
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)#transparrency, 0 transparente 255 solid
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



"""
Responsável por gráficos do jogo
"""

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("purple")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        """    piece = board[r][c]
            if piece != "--": #quadrado nao vazio
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))"""

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # quadrado nao vazio
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
animação
"""

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #drawwmoving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText (screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":
    main()

