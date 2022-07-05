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

    loadImages()
    running = True
    sqSelected = () #no square selected, keep track of the last click of the user
    playerClicks = [] #keep track of the player ckicks, dois tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            ##mouse selecao
            elif e.type == p.MOUSEBUTTONDOWN:
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
                            sqSelected = () ##reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: ##desfaz se z é pressionado
                    gs.undoMove()
                    moveMade=True


        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsável por gráficos do jogo
"""

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
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



if __name__ == "__main__":
    main()

