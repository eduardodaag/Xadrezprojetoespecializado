#jogo será rodado aqui

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 ##Tamanho pixels tab, dimensão do tabuleiro
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] ##carrega as imagens
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))

"""

Caminho principal do jogo

"""

def main():
    p.init() #inicia pygame
    screen = p.display.set_mode((WIDTH, HEIGHT)) ##define tela e clock
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() ## inicializa jogo
    validMoves = gs.getValidMoves() #movimento valido para cada peça
    moveMade = False #flag para movimento
    animate = False #flag para animação
    loadImages() #carrega as peças no tabuleiro
    running = True
    sqSelected = () #no square selected, mantem track dos clicks do usuario - quadrados selecionados
    playerClicks = [] #track dos cliques na tela
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False ##sair do jogo

            ##mouse selecao
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #localizacao do mouse
                    col = location[0]//SQ_SIZE ##linha e coluna selecionada
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): ##user selecionou mesmo quadrado:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) ##acrescenta o quadrado selecionado
                    if len(playerClicks) == 2: #depois do 2o clique
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) ##parametros do movimento
                        print(move.getChessNotation()) #printa o movimento
                        for i in range(len(validMoves)): #se o selecionado estiver dentro dos movimentos válidos
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i]) ##faz o movimento e flag que foi feito
                                moveMade=True
                                animate = True
                                sqSelected = () ##reseta as escolhar
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected] #se nao fez o movimento, altera o último clique pra peça inicial

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: ##desfaz se z é pressionado
                    gs.undoMove() #desfaz movimento
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reseta jogo
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate: #animacao do movimento
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves=gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState(screen, gs, validMoves, sqSelected) #atualiza o visual do jogo

        if gs.checkMate: ##checkmate fim de jogo
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")

        elif gs.staleMate:
            drawText(screen, "Draw")

        clock.tick(MAX_FPS)
        p.display.flip() #reseta jogo

"""
Highlight no quadrado escolhido e mostra movimentos disponíveis
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != (): #se algum quadrado foi selecionado
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #descobre quem joga
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)#transparência
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight movimentos possíveis
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
    colors = [p.Color("white"), p.Color("lemonchiffon3")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        """    piece = board[r][c]
            if piece != "--": #quadrado nao vazio
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))"""

def drawPieces(screen, board): ##desenho das imagens
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] #peça com base na posição inicial dela
            if piece != "--":  # quadrado nao vazio
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
animação
"""

def animateMove(move, screen, board, clock): ##animacao do movimento
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


def drawText (screen, text): ##texto de vencedor
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":
    main()

