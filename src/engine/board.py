from typing import List
from src.engine.piece import (
    Piece, PieceColor, Pawn, Knight, Bishop, Rook, Queen, King )


class BoardPosition:
    """Stores a chess board position's rank, file, and piece (if any)."""
    __slots__ = ("rank", "file", "piece")

    def __init__(self, rank: chr, file: int, piece: Piece = None) -> None:
        self.rank = rank
        self.file = file
        self.piece = None

    def __str__(self) -> str:
        # if self.piece:
        #     return str(self.piece)
        # return "."
        return f"{self.rank}{self.file}"
    
    def position(self) -> tuple:
        """Returns the position as a (character, integer) tuple."""
        return (self.rank, self.file)
    
    def set_piece(self, new_piece) -> bool:
        self.piece = new_piece


class Board:
    """Store information on the location of each piece."""
    __slots__ = ("squares", "current_turn")
    
    def __init__(self):
        print("WARNING: Moves not yet validated. A player can put themself in check!")
        print("WARNING: Castling not yet implemented.")
        print("WARNING: en passant not yet implemented.")
        self.squares = tuple(tuple(BoardPosition(rank, file)
                                   for rank in self.all_ranks())
                             for file in self.all_files())
        self.reset_board()
        self.current_turn = PieceColor.WHITE
        
    def __str__(self) -> str:
        return ("\n".join([" ".join([str(square) for square in rank]) 
            for rank in reversed(self.squares)]))
    
    def all_ranks(self) -> tuple():
        return tuple(chr(ord('a')+i) for i in range(8))
    
    def all_files(self) -> tuple():
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

    def move_piece(self, old: BoardPosition, new: BoardPosition) -> None:
        piece = old.piece
        piece.move()
        new.set_piece(piece)
        old.set_piece(None)

    def change_turn(self) -> PieceColor:
        if self.current_turn is PieceColor.WHITE:
            self.current_turn = PieceColor.BLACK
            return PieceColor.BLACK
        self.current_turn = PieceColor.WHITE
        return PieceColor.WHITE

    def get_legal_moves(self, position: BoardPosition) -> List[BoardPosition]:
        if not position.piece:
            return []
        if position.piece.__class__ is Pawn:
            return self.get_legal_pawn_moves(position)
        elif position.piece.__class__ is Knight:
            return self.get_legal_knight_moves(position)
        elif position.piece.__class__ is Bishop:
            return self.get_legal_bishop_moves(position)
        elif position.piece.__class__ is Rook:
            return self.get_legal_rook_moves(position)
        elif position.piece.__class__ is Queen:
            return self.get_legal_queen_moves(position)
        elif position.piece.__class__ is King:
            return self.get_legal_king_moves(position)
        return []
        
    def get_legal_pawn_moves(self, position: BoardPosition) -> List[BoardPosition]:
        pawn_moves = []
        pawn = position.piece
        color = pawn.color
        direction = pawn.direction
        rank = position.rank
        file = position.file
        square = self.square_at(rank, file+direction)
        # Move forward one
        if not square.piece:
            pawn_moves.append(square)
        # Move forward two
        square = self.square_at(rank, file+(2*direction))
        if not square.piece and pawn.has_not_moved:
            pawn_moves.append(square)
        # Capture to left
        if rank >= 'b':
            prev_rank = chr(ord(rank)-1)
            square = self.square_at(prev_rank, file+direction)
            if square.piece and square.piece.color is not color:
                pawn_moves.append(square)
        # Capture to right
        if rank <= 'g':
            next_rank = chr(ord(rank)+1)
            square = self.square_at(next_rank, file+direction)
            if square.piece and square.piece.color is not color:
                pawn_moves.append(square)
        return pawn_moves
    
    def get_legal_knight_moves(self, position: BoardPosition) -> List[BoardPosition]:
        knight_moves = []
        knight = position.piece
        color = knight.color
        rank = position.rank
        file = position.file
        # Left two down one, left two up one
        if ord(rank) >= ord('c'):
            rank_two_left = chr(ord(rank)-2)
            if file >= 2:
                square = self.square_at(rank_two_left, file-1)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
            if file <= 7:
                square = self.square_at(rank_two_left, file+1)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
        # Left one down two, left one up two
        if ord(rank) >= ord('b'):
            rank_one_left = chr(ord(rank)-1)
            if file >= 3:
                square = self.square_at(rank_one_left, file-2)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
            if file <= 6:
                square = self.square_at(rank_one_left, file+2)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
        # Right two down one, right two up one
        if ord(rank) <= ord('f'):
            rank_two_right = chr(ord(rank)+2)
            if file >= 2:
                square = self.square_at(rank_two_right, file-1)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
            if file <= 7:
                square = self.square_at(rank_two_right, file+1)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
        # Right one down two, right one up two
        if ord(rank) <= ord('g'):
            rank_one_right = chr(ord(rank)+1)
            if file >= 3:
                square = self.square_at(rank_one_right, file-2)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
            if file <= 6:
                square = self.square_at(rank_one_right, file+2)
                if not square.piece or square.piece.color is not color:
                    knight_moves.append(square)
        return knight_moves       

    def get_legal_bishop_moves(self, position: BoardPosition) -> List[BoardPosition]:
        bishop_moves = []
        bishop = position.piece
        color = bishop.color
        rank = position.rank
        file = position.file
        # Up-left diagonal
        current_rank = chr(ord(rank)-1)
        current_file = file+1
        while current_rank >= 'a' and current_file <= 8:
            square = self.square_at(current_rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                bishop_moves.append(square)
                break
            bishop_moves.append(square)
            current_rank = chr(ord(current_rank)-1)
            current_file = current_file+1
        # Down-left diagonal
        current_rank = chr(ord(rank)-1)
        current_file = file-1
        while current_rank >= 'a' and current_file >= 1:
            square = self.square_at(current_rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                bishop_moves.append(square)
                break
            bishop_moves.append(square)
            current_rank = chr(ord(current_rank)-1)
            current_file = current_file-1
        # Down-right diagonal
        current_rank = chr(ord(rank)+1)
        current_file = file-1
        while current_rank <= 'h' and current_file >= 1:
            square = self.square_at(current_rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                bishop_moves.append(square)
                break
            bishop_moves.append(square)
            current_rank = chr(ord(current_rank)+1)
            current_file = current_file-1
        # Up-right diagonal
        current_rank = chr(ord(rank)+1)
        current_file = file+1
        while current_rank <= 'h' and current_file <= 8:
            square = self.square_at(current_rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                bishop_moves.append(square)
                break
            bishop_moves.append(square)
            current_rank = chr(ord(current_rank)+1)
            current_file = current_file+1
        return bishop_moves

    def get_legal_rook_moves(self, position: BoardPosition) -> List[BoardPosition]:
        rook_moves = []
        rook = position.piece
        color = rook.color
        rank = position.rank
        file = position.file
        # Left
        current_rank = chr(ord(rank)-1)
        while current_rank >= 'a':
            square = self.square_at(current_rank, file)
            if square.piece:
                if square.piece.color is color:
                    break
                rook_moves.append(square)
                break
            rook_moves.append(square)
            current_rank = chr(ord(current_rank)-1)
        # Right
        current_rank = chr(ord(rank)+1)
        while current_rank <= 'h':
            square = self.square_at(current_rank, file)
            if square.piece:
                if square.piece.color is color:
                    break
                rook_moves.append(square)
                break
            rook_moves.append(square)
            current_rank = chr(ord(current_rank)+1)
        # Up
        current_file = file+1
        while current_file <= 8:
            square = self.square_at(rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                rook_moves.append(square)
                break
            rook_moves.append(square)
            current_file = current_file+1
        # Down
        current_file = file-1
        while current_file >= 1:
            square = self.square_at(rank, current_file)
            if square.piece:
                if square.piece.color is color:
                    break
                rook_moves.append(square)
                break
            rook_moves.append(square)
            current_file = current_file-1
        return rook_moves

    def get_legal_queen_moves(self, position: BoardPosition) -> List[BoardPosition]:
        bishop_moves = self.get_legal_bishop_moves(position)
        rook_moves = self.get_legal_rook_moves(position)
        return bishop_moves + rook_moves
        
    def get_legal_king_moves(self, position: BoardPosition) -> List[BoardPosition]:
        king_moves = []
        king = position.piece
        color = king.color
        rank = position.rank
        file = position.file
        if (ord(rank) >= ord('b')):
            if file >= 2:
                square = self.square_at(chr(ord(rank)-1), file-1)
                if not square.piece or square.piece.color is not color:
                    king_moves.append(square)
            if file <= 7:
                square = self.square_at(chr(ord(rank)-1), file+1)
                if not square.piece or square.piece.color is not color:
                    king_moves.append(square)
            square = self.square_at(chr(ord(rank)-1), file)
            if not square.piece or square.piece.color is not color:
                king_moves.append(square)
        if (ord(rank) <= ord('g')):
            if file >= 2:
                square = self.square_at(chr(ord(rank)+1), file-1)
                if not square.piece or square.piece.color is not color:
                    king_moves.append(square)
            if file <= 7:
                square = self.square_at(chr(ord(rank)+1), file+1)
                if not square.piece or square.piece.color is not color:
                    king_moves.append(square)
            square = self.square_at(chr(ord(rank)+1), file)
            if not square.piece or square.piece.color is not color:
                king_moves.append(square)
        if file >= 2:
            square = self.square_at(rank, file-1)
            if not square.piece or square.piece.color is not color:
                king_moves.append(square)
        if file <= 7:
            square = self.square_at(rank, file+1)
            if not square.piece or square.piece.color is not color:
                king_moves.append(square)
        return king_moves

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

