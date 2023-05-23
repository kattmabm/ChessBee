import pygame
from src.engine.board import Board, BoardPosition
from src.ui.pieceAssets import drawPiece
from src.ui.color import Color
from src.ui.window import Window


class SquareColor:
    LIGHT = Color.BOARD_LIGHT
    DARK  = Color.BOARD_DARK


class SquareComponent:
    __slots__ = ("position", "rank", "file", "dark", "selected",
                 "highlighted", "rect", "xmin", "ymin")

    def __init__(self, boardPosition: BoardPosition):
        self.position = boardPosition
        self.selected = False
        self.highlighted = False
        self.rank = self.position.rank
        self.file = self.position.file
        self.dark = False if self.file % 2 == 0 else True
        if self.rank in ('b', 'd', 'f', 'h'):
            self.dark = not self.dark
        size = Window.SQUARE_SIZE
        self.xmin = Window.BOARD_XMIN + size*(ord(self.rank)-ord('a'))
        self.ymin = Window.BOARD_YMIN + size*(8-self.file)
        self.rect = pygame.Rect(self.xmin, self.ymin, size, size)

    def color(self) -> SquareColor:
        if self.selected:
            return Color.BOARD_BLUE
        if self.dark:
            if self.highlighted:
                return Color.BOARD_LIGHT_G
            return Color.BOARD_LIGHT
        if self.highlighted:
            return Color.BOARD_DARK_G
        return Color.BOARD_DARK


class BoardComponent:
    __slots__ = ("board", "window", "squares", "selected_square_pos")

    def __init__(self, window: pygame.Surface):
        self.window = window
        self.board = Board()
        self.board.reset_board()
        self.squares = tuple(tuple(SquareComponent(square) 
                                   for square in rank) 
                                   for rank in self.board.squares)
        self.selected_square_pos = None
        
    def draw(self) -> None:
        for rank in self.squares:
            for square in rank:
                pygame.draw.rect(self.window, square.color(), square.rect)
                drawPiece(square.position.piece, self.window,
                          square.xmin, square.ymin)
                
    def select_square_at(self, rank: chr, file: int) -> None:
        self.selected_square_pos = self.board.square_at(rank, file)
        rank = ord(rank) - ord('a')
        file = file - 1
        self.squares[file][rank].selected = True

    def hl_square_at(self, rank: chr, file: int) -> None:
        rank = ord(rank) - ord('a')
        file = file - 1
        self.squares[file][rank].highlighted = True

    def clear_colors(self):
        self.selected_square_pos = None
        for rank in self.squares:
            for square in rank:
                square.selected = False
                square.highlighted = False

