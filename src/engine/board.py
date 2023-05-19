from src.engine.piece import (
    Piece, PieceColor, Pawn, Knight, Bishop, Rook, Queen, King
)


class BoardPosition:
    """Stores a chess piece's rank and file.

    Constructor:

        BoardPosition(rank, file)

    Functions:

        rank()     -> chr
        file()     -> int
        position() -> (chr, int)
    """
    def __init__(self, rank: chr, file: int) -> None:
        self.rank = rank
        self.file = file
        self.piece = None

    def __str__(self) -> str:
        if self.piece:
            return str(self.piece)
        return "."
        # return f"{self.rank}{self.file}"
    
    def rank(self) -> chr:
        """Returns the position's rank as a character."""
        return self.rank
    
    def file(self) -> int:
        """Returns the position's file as an integer."""
        return self.file
    
    def position(self) -> tuple:
        """Returns the position as a (character, integer) tuple."""
        return (self.rank, self.file)
    
    def piece(self) -> Piece:
        return self.piece
    
    def set_piece(self, new_piece) -> bool:
        self.piece = new_piece


class Board:
    """Store information on the location of each piece."""
    def __init__(self):
        self.squares = tuple(tuple(BoardPosition(rank, file)
                                   for rank in self.all_ranks())
                             for file in self.all_files())
        self.reset_board()
        
    def __str__(self) -> str:
        return ("\n".join([" ".join([str(square) for square in rank]) 
            for rank in reversed(self.squares)]))
    
    def all_ranks(self) -> tuple:
        return tuple(chr(ord('a')+i) for i in range(8))
    
    def all_files(self) -> tuple:
        return tuple(i+1 for i in range(8))
    
    def print_squares(self) -> None:
        print("\n".join([" ".join([str(square) for square in rank]) 
            for rank in reversed(self.squares)]))
        
    def square_at(self, rank: chr, file: int) -> BoardPosition:
        rank = ord(rank)-ord('a')
        file = file-1
        return self.squares[file][rank]
    
    def place_piece_at(self, piece: Piece, rank: chr, file: int) -> bool:
        square = self.square_at(rank, file)
        return square.set_piece(piece)
    
    def move_piece_to(self, piece: Piece, rank: chr, file: int) -> bool:
        square = self.square_at(rank, file)
        if square.piece():
            return False
        square.set_piece(piece)

    def capture_piece_at(self, piece: Piece, rank: chr, file: int) -> bool:
        square = self.square_at(rank, file)
        target_piece = square.piece()
        if target_piece and piece.color() is not target_piece.color():
            square.set_piece(piece)

    def reset_board(self) -> None:
        for rank in self.all_ranks():
            for file in self.all_files():
                self.square_at(rank, file).set_piece(None)
        # Pawns
        for rank in self.all_ranks():
            self.square_at(rank, 2).set_piece(Pawn(PieceColor.WHITE))
            self.square_at(rank, 7).set_piece(Pawn(PieceColor.BLACK))
        # Rooks
        self.square_at('a', 1).set_piece(Rook(PieceColor.WHITE))
        self.square_at('h', 1).set_piece(Rook(PieceColor.WHITE))
        self.square_at('a', 8).set_piece(Rook(PieceColor.BLACK))
        self.square_at('h', 8).set_piece(Rook(PieceColor.BLACK))
        # Knights
        self.square_at('b', 1).set_piece(Knight(PieceColor.WHITE))
        self.square_at('g', 1).set_piece(Knight(PieceColor.WHITE))
        self.square_at('b', 8).set_piece(Knight(PieceColor.BLACK))
        self.square_at('g', 8).set_piece(Knight(PieceColor.BLACK))
        # Bishops
        self.square_at('c', 1).set_piece(Bishop(PieceColor.WHITE))
        self.square_at('f', 1).set_piece(Bishop(PieceColor.WHITE))
        self.square_at('c', 8).set_piece(Bishop(PieceColor.BLACK))
        self.square_at('f', 8).set_piece(Bishop(PieceColor.BLACK))
        # Queens
        self.square_at('d', 1).set_piece(Queen(PieceColor.WHITE))
        self.square_at('d', 8).set_piece(Queen(PieceColor.BLACK))
        # Kings
        self.square_at('e', 1).set_piece(King(PieceColor.WHITE))
        self.square_at('e', 8).set_piece(King(PieceColor.BLACK))

