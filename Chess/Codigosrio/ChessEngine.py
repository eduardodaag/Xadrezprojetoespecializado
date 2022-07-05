"""
Definir os movimentos possíveis e etc

"""

class GameState():
    def __init__(self):

        #tabuleiro 8x8, 2d, cada um possui 2 letras pra representar as peças. Cor / peça.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False



    #Take a move as parameter and executes

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.WhiteToMove = not self.whiteToMove #muda jogador

        #atualiza a localização do rei
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)


    #pawn promotion

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved [0] + 'Q'



    #undo last move

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            # atualiza a localização do rei se preciso
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    All moves considering checks
    
    """
    def getValidMoves(self):

        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #movimento invalido se atacar o rei
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: #cheque ou cheque-mate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    #verifica se o jogador esta em cheque
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return  self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #determina se o inimigo pode avançar para o espaço (r,c)
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch oponnents turn
        opMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch oponnents turn back

        for move in opMoves:
            if move.endRow == r and move.endCol == c: #espaço sobre ataque
                return True
        return False

    """
    All moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number rows
            for c in range(len(self.board[r])): #number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #chama a função de movimentação de peça apropriada
        return moves

    def getPawnMoves(self, r, c, moves):
        # existem 3 tipos de movimentos possiveis para os peões

        if self.whiteToMove:  # White pawn moves

            if self.board[r - 1][c] == "--":  # verifica se o quadrado da frente esta vazio(row) e avança
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance se nao tiver nada na frente
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # conferir que não vai extrapolar as colunas (captures to the left)
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))  # move linha e coluna
            if c + 1 <= 7:  # (captures to the right)
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves

            if self.board[r + 1][c] == "--":  # verifica se o quadrado da frente esta vazio(row) e avança
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance se nao tiver nada na frente
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # conferir que não vai extrapolar as colunas (captures to the left)
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))  # move linha e coluna
            if c + 1 <= 7:  # (captures to the right)
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    def getKnightMoves(self, r, c, moves):
        KnightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in KnightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # change diagonally
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # bishop can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        KingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + KingMoves[i][0]
            endCol = c + KingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))



class Move():
    #maps keys to values, key : value

    ranksToRows = {"1": 7, "2":6, "3": 5, "4":4, "5":3, "6":2, "7":1, "8":0} #transformando da posicao do pc pra posicao pro xadrezgg
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b":1, "c": 2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """overriding the equal method"""

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID==other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




