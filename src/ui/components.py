import pygame
from src.engine.board import Board, BoardPosition
from src.engine.piece import Piece
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
    __slots__ = ("position", "color", "rect")

    def __init__(self, boardPosition: BoardPosition):
        self.position = boardPosition
        # Get square's rank and file
        rank = self.position.rank
        file = self.position.file
        # Calculate color the square should be
        self.color = SquareColor.DARK if file % 2 == 0 else SquareColor.LIGHT
        if rank in ('b', 'd', 'f', 'h'):
            self.toggle_color()
        # Position the window
        size = Window.SQUARE_SIZE
        xmin = Window.BOARD_XMIN + size*(ord(rank)-ord('a'))
        ymin = Window.BOARD_YMIN + size*(file-1)
        self.rect = pygame.Rect(xmin, ymin, size, size)

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