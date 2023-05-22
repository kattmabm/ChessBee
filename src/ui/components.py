import pygame
from src.engine.board import Board, BoardPosition
from src.ui.pieces import PieceAssets, drawPiece
from src.ui.color import Color
from src.ui.window import Window


class SquareColor:
    LIGHT = Color.BOARD_LIGHT
    DARK  = Color.BOARD_DARK

def toggle_color(color: SquareColor) -> SquareColor:
    if color is SquareColor.LIGHT:
        return SquareColor.DARK
    return SquareColor.LIGHT


class SquareComponent:
    __slots__ = ("position", "color", "rect", "xmin", "ymin")

    def __init__(self, boardPosition: BoardPosition):
        self.position = boardPosition
        # Get square's rank and file
        rank = self.position.rank
        file = self.position.file
        # Calculate color the square should be
        self.color = SquareColor.LIGHT if file % 2 == 0 else SquareColor.DARK
        if rank in ('b', 'd', 'f', 'h'):
            self.toggle_color()
        # Position the window
        size = Window.SQUARE_SIZE
        self.xmin = Window.BOARD_XMIN + size*(ord(rank)-ord('a'))
        self.ymin = Window.BOARD_YMIN + size*(8-file)
        self.rect = pygame.Rect(self.xmin, self.ymin, size, size)

    def toggle_color(self) -> None:
        if self.color is SquareColor.LIGHT:
            self.color = SquareColor.DARK
        else:
            self.color = SquareColor.LIGHT


class BoardComponent:
    __slots__ = ("board", "window", "squareComponents")

    def __init__(self, window: pygame.Surface):
        self.window = window
        self.board = Board()
        self.board.reset_board()
        print(self.board)
        self.squareComponents = tuple(tuple(SquareComponent(square)
                                            for square in rank)
                                            for rank in self.board.squares)
        
    def draw(self):
        for rank in self.squareComponents:
            for square in rank:
                pygame.draw.rect(self.window, square.color, square.rect)
                drawPiece(square.position.piece, self.window, square.xmin, square.ymin)
                