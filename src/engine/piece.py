from abc import ABC, abstractmethod


class PieceColor:
    WHITE = 0
    BLACK = 1


class TextColor:
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    END = "\033[0m"


class Piece(ABC):
    """Abstract class detailing the properties of a chess piece."""
    def __str__(self) -> str:
        if self.color == PieceColor.WHITE:
            return TextColor.YELLOW + self.fen_char() + TextColor.END
        return TextColor.BLUE + self.fen_char() + TextColor.END

    def fen_char(self) -> chr:
        """Returns the character representing this piece in FEN notation."""
        pass

    def value(self) -> int:
        """Returns the value of a piece in points of material."""
        pass
    
    def color(self) -> PieceColor:
        """Returns the color of a piece."""
        return self.color
    
    @abstractmethod
    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        pass

    @abstractmethod
    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        pass


class Pawn(Piece):
    """Class detailing the behavior of a pawn."""
    def __init__(self, color: PieceColor):
        self.color = color
        self.direction = 1 if color == PieceColor.WHITE else -1
        self.has_not_moved = True
    
    def fen_char(self) -> chr:
        return 'p'
    
    def value(self) -> int:
        return 1
    
    def move(self) -> None:
        self.has_not_moved = False

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        moves = [(rank, file+self.direction)]
        if not self.has_not_moved:
            moves.append((rank, file+(2*self.direction)))
        return moves

    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        captures = []
        cap_file = file + self.direction
        if ord(rank) > ord('a'):
            captures.append((chr(ord(rank)-1), cap_file))
        if ord(rank) < ord('h'):
            captures.append((chr(ord(rank)-1), cap_file))
        return captures


class Knight(Piece):
    """Class detailing the behavior of a knight."""
    def __init__(self, color: PieceColor):
        self.color = color
    
    def fen_char(self) -> chr:
        return 'N'
    
    def value(self) -> int:
        return 3
    
    def move(self) -> None:
        return

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can move to."""
        moves = []
        if ord(rank) >= ord('c'):
            if file >= 2:
                moves.append[(chr(ord(rank)-2), file-1)]
            if file <= 7:
                moves.append[(chr(ord(rank)-2), file+1)]
        if ord(rank) >= ord('b'):
            if file >= 3:
                moves.append[(chr(ord(rank)-1), file-2)]
            if file <= 6:
                moves.append[(chr(ord(rank)-1), file+2)]
        if ord(rank) <= ord('f'):
            if file >= 2:
                moves.append[(chr(ord(rank)+2), file-1)]
            if file <= 7:
                moves.append[(chr(ord(rank)+2), file+1)]
        if ord(rank) >= ord('g'):
            if file >= 3:
                moves.append[(chr(ord(rank)+1), file-2)]
            if file <= 6:
                moves.append[(chr(ord(rank)+1), file+2)]
        return moves


    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can capture a piece on."""
        return self.possible_moves(rank, file)


class Bishop(Piece):
    """Class detailing the behavior of a bishop."""
    def __init__(self, color: PieceColor):
        self.color = color
    
    def fen_char(self) -> chr:
        return 'B'
    
    def value(self) -> int:
        return 3
    
    def move(self) -> None:
        return

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can move to."""
        moves = []
        r = ord(rank) - 1
        f = file - 1
        while r >= ord('a') and f >= 1:
            moves.append[(chr(r), f)]
            r -= 1
            f -= 1
        r = ord(rank) + 1
        f = file - 1
        while r <= ord('h') and f >= 1:
            moves.append[(chr(r), f)]
            r += 1
            f -= 1
        r = ord(rank) + 1
        f = file + 1
        while r <= ord('h') and f <= 8:
            moves.append[(chr(r), f)]
            r += 1
            f += 1
        r = ord(rank) - 1
        f = file + 1
        while r >= ord('a') and f <= 8:
            moves.append[(chr(r), f)]
            r -= 1
            f += 1
        return moves

    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can capture a piece on."""
        return self.possible_moves(rank, file)
    

class Rook(Piece):
    """Class detailing the behavior of a rook."""
    def __init__(self, color: PieceColor):
        self.color = color
        self.has_not_moved = True
    
    def fen_char(self) -> chr:
        return 'R'
    
    def value(self) -> int:
        return 5
    
    def move(self) -> None:
        self.has_not_moved = False

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can move to."""
        moves = []
        for r in range(ord('a'), ord('h')+1):
            if r == ord(rank):
                continue
            moves.append((chr(r), file))
        for f in range(8):
            if f+1 == file:
                continue
            moves.append((rank, f+1))

    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can capture a piece on."""
        return self.possible_moves(rank, file)
    
    def can_castle(self) -> bool:
        return self.has_not_moved
    

class Queen(Piece):
    """Class detailing the behavior of a queen."""
    def __init__(self, color: PieceColor):
        self.color = color
    
    def fen_char(self) -> chr:
        return 'Q'
    
    def value(self) -> int:
        return 9
    
    def move(self) -> None:
        return

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can move to."""
        moves = []
        r = ord(rank) - 1
        f = file - 1
        while r >= ord('a') and f >= 1:
            moves.append[(chr(r), f)]
            r -= 1
            f -= 1
        r = ord(rank) + 1
        f = file - 1
        while r <= ord('h') and f >= 1:
            moves.append[(chr(r), f)]
            r += 1
            f -= 1
        r = ord(rank) + 1
        f = file + 1
        while r <= ord('h') and f <= 8:
            moves.append[(chr(r), f)]
            r += 1
            f += 1
        r = ord(rank) - 1
        f = file + 1
        while r >= ord('a') and f <= 8:
            moves.append[(chr(r), f)]
            r -= 1
            f += 1
        for r in range(ord('a'), ord('h')+1):
            if r == ord(rank):
                continue
            moves.append((chr(r), file))
        for f in range(8):
            if f+1 == file:
                continue
            moves.append((rank, f+1))
        return moves

    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can capture a piece on."""
        return self.possible_moves(rank, file)


class King(Piece):
    """Class detailing the behavior of a king."""
    def __init__(self, color: PieceColor):
        self.color = color
        self.has_not_moved = True
    
    def fen_char(self) -> chr:
        return 'K'
    
    def value(self) -> int:
        return 5
    
    def move(self) -> None:
        self.has_not_moved = False

    def possible_moves(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can move to."""
        moves = []
        return moves

    def possible_captures(self, rank: chr, file: int) -> list[tuple]:
        """Returns a list of all valid position tuples that this piece
        can capture a piece on."""
        return self.possible_moves(rank, file)
    
    def can_castle(self) -> bool:
        return self.has_not_moved

