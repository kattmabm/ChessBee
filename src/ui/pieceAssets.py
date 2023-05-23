import pygame
from os import path
from src.engine.piece import (
    Piece, PieceColor, Pawn, Knight, Bishop, Rook, Queen, King )
from src.ui.window import Window

SIZE = (Window.SQUARE_SIZE, Window.SQUARE_SIZE)

def drawPiece(piece: Piece, surface: pygame.surface.Surface,
              xmin: int, ymin: int) -> None:
    if piece.__class__ is Pawn:
        if piece.color == PieceColor.WHITE:
            surface.blit(PieceAssets.PAWN_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.PAWN_BLACK, (xmin, ymin))
    elif piece.__class__ is Knight:
        if piece.color is PieceColor.WHITE:
            surface.blit(PieceAssets.KNIGHT_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.KNIGHT_BLACK, (xmin, ymin))
    elif piece.__class__ is Bishop:
        if piece.color is PieceColor.WHITE:
            surface.blit(PieceAssets.BISHOP_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.BISHOP_BLACK, (xmin, ymin))
    elif piece.__class__ is Rook:
        if piece.color is PieceColor.WHITE:
            surface.blit(PieceAssets.ROOK_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.ROOK_BLACK, (xmin, ymin))
    elif piece.__class__ is Queen:
        if piece.color is PieceColor.WHITE:
            surface.blit(PieceAssets.QUEEN_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.QUEEN_BLACK, (xmin, ymin))
    elif piece.__class__ is King:
        if piece.color is PieceColor.WHITE:
            surface.blit(PieceAssets.KING_WHITE, (xmin, ymin))
        else:
            surface.blit(PieceAssets.KING_BLACK, (xmin, ymin))
    

class PieceAssets:
    PAWN_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets","PawnWhite.png")), SIZE)
    PAWN_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "PawnBlack.png")), SIZE)
    KNIGHT_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "KnightWhite.png")), SIZE)
    KNIGHT_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "KnightBlack.png")), SIZE)
    BISHOP_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "BishopWhite.png")), SIZE)
    BISHOP_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "BishopBlack.png")), SIZE)
    ROOK_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "RookWhite.png")), SIZE)
    ROOK_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "RookBlack.png")), SIZE)
    QUEEN_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "QueenWhite.png")), SIZE)
    QUEEN_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "QueenBlack.png")), SIZE)
    KING_WHITE = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "KingWhite.png")), SIZE)
    KING_BLACK = pygame.transform.scale(pygame.image.load(
        path.join("src", "ui", "assets", "KingBlack.png")), SIZE)

