import pygame
from src.engine.board import Board, BoardPosition
from src.engine.piece import PieceColor
from src.ui.color import Color
from src.ui.window import Window


class SquareColor:
    WHITE = 0
    BLACK = 1


class SquareComponent:
    __slots__ = ("rank", "file", "color", "position")

    def __init__(self, rank: chr, file: int, color: SquareColor):
        self.rank = rank
        self.file = file
        self.color = color
        self.boardPosition = BoardPosition(rank, file)
        size = Window.SQUARE_SIZE
        xmin = Window.BOARD_XMIN + size*(ord(rank)-ord('a'))
        ymin = Window.BOARD_YMIN + size*(file-1)
        self.rect = pygame.Rect(xmin, ymin, size, size)


class BoardComponent:
    __slots__ = ("board")

    def __init__(self):
        self.board = Board()
        self.board.reset_board()
        print(self.board)