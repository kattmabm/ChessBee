import pygame
from src.engine.board import Board, BoardPosition
from src.ui.pieceAssets import drawPiece
from src.ui.color import Color
from src.ui.text import Label
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
    __slots__ = ("board", "window", "squares", "selected_square_pos",
                 "rank_labels")

    def __init__(self, window: pygame.Surface):
        self.window = window
        self.board = Board()
        self.board.reset_board()
        self.squares = tuple(tuple(SquareComponent(square) 
                                   for square in rank) 
                                   for rank in self.board.squares)
        self.rank_labels = RankFileLabels(self)
        self.selected_square_pos = None
        
    def draw(self) -> None:
        for rank in self.squares:
            for square in rank:
                pygame.draw.rect(self.window, square.color(), square.rect)
                drawPiece(square.position.piece, self.window,
                          square.xmin, square.ymin)
        self.rank_labels.draw()
                
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


class RankFileLabels:
    __slots__ = ("window", "rank_labels", "file_labels")

    def __init__(self, board: BoardComponent):
        self.window = board.window
        all_ranks = board.board.all_ranks()
        all_files = board.board.all_files()
        self.rank_labels = []
        self.file_labels = []
        size = Window.SQUARE_SIZE
        font_size = 20
        offset = 5
        for rank in all_ranks:
            xcenter = Window.BOARD_XMIN + size*(ord(rank)-ord('a') + 1/2)
            ycenter = Window.BOARD_YMIN + 8*size + font_size/2 + offset
            rank_label = Label(self.window, rank, xcenter, ycenter, font_size)
            self.rank_labels.append(rank_label)
        for file in all_files:
            xcenter = Window.BOARD_XMIN - font_size/2 - offset
            ycenter = Window.BOARD_YMIN + size*(8-file + 1/2)
            file_label = Label(self.window, str(file), xcenter, ycenter, font_size)
            self.file_labels.append(file_label)

    def draw(self):
        for rank_label in self.rank_labels:
            self.window.blit(rank_label.image, rank_label.rect)
        for file_label in self.file_labels:
            self.window.blit(file_label.image, file_label.rect)

