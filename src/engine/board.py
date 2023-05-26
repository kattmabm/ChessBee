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


class GameStatus:
    PLAY = 0
    CHECKMATE = 1
    STALEMATE = 2


class Board:
    """Store information on the location of each piece."""
    __slots__ = ("squares", "current_turn", "current_move")
    
    def __init__(self):
        self.squares = tuple(tuple(BoardPosition(rank, file)
                                   for rank in self.all_ranks())
                             for file in self.all_files())
        self.reset_board()
        self.current_turn = PieceColor.WHITE
        self.current_move = 0
        
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
        # If this is en passant, remove the pawn at the old position
        if piece.__class__ is Pawn:
            if not old.rank == new.rank and not new.piece:
                self.square_at(new.rank, old.file).piece = None
        # If this is castling, move both the king and rook
        if piece.__class__ is King:
            rank_diff = ord(new.rank) - ord(old.rank)
            if rank_diff == -2:
                # Castling queenside
                self.square_at('a', old.file).piece = None
                self.square_at('d', old.file).piece = Rook(piece.color, False)
            elif rank_diff == 2:
                # Castling kingside
                self.square_at('h', old.file).piece = None
                self.square_at('f', old.file).piece = Rook(piece.color, False)
        piece.move(self.current_move)
        new.piece = old.piece
        old.piece = None
        self.current_move += 1

    def change_turn(self) -> PieceColor:
        if self.current_turn is PieceColor.WHITE:
            self.current_turn = PieceColor.BLACK
            return PieceColor.BLACK
        self.current_turn = PieceColor.WHITE
        return PieceColor.WHITE

    def get_legal_moves(self, position: BoardPosition, shallow=False) -> List[BoardPosition]:
        moves = []
        if position.piece.__class__ is Pawn:
            moves = self.get_pawn_moves(position)
        elif position.piece.__class__ is Knight:
            moves = self.get_knight_moves(position)
        elif position.piece.__class__ is Bishop:
            moves = self.get_bishop_moves(position)
        elif position.piece.__class__ is Rook:
            moves = self.get_rook_moves(position)
        elif position.piece.__class__ is Queen:
            moves = self.get_queen_moves(position)
        elif position.piece.__class__ is King:
            moves = self.get_king_moves(position, shallow)
        if shallow:
            return moves
        return self.validate_moves(position, moves)
        
    def get_pawn_moves(self, position: BoardPosition) -> List[BoardPosition]:
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
        if not square.piece and not pawn.last_moved:
            pawn_moves.append(square)
        # Capture to left
        if rank >= 'b':
            prev_rank = chr(ord(rank)-1)
            square = self.square_at(prev_rank, file+direction)
            if square.piece and square.piece.color is not color:
                pawn_moves.append(square)
            # En passant left
            adj_square = self.square_at(prev_rank, file)
            if (adj_square.piece and adj_square.piece.__class__ is Pawn and
                    adj_square.piece.color is not color and
                    self.current_move - adj_square.piece.last_moved == 1):
                pawn_moves.append(square)
        # Capture to right
        if rank <= 'g':
            next_rank = chr(ord(rank)+1)
            square = self.square_at(next_rank, file+direction)
            if square.piece and square.piece.color is not color:
                pawn_moves.append(square)
            # En passant right
            adj_square = self.square_at(next_rank, file)
            if (adj_square.piece and adj_square.piece.__class__ is Pawn and
                    adj_square.piece.color is not color and
                    self.current_move - adj_square.piece.last_moved == 1):
                pawn_moves.append(square)
        return pawn_moves
    
    def get_knight_moves(self, position: BoardPosition) -> List[BoardPosition]:
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

    def get_bishop_moves(self, position: BoardPosition) -> List[BoardPosition]:
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

    def get_rook_moves(self, position: BoardPosition) -> List[BoardPosition]:
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

    def get_queen_moves(self, position: BoardPosition) -> List[BoardPosition]:
        bishop_moves = self.get_bishop_moves(position)
        rook_moves = self.get_rook_moves(position)
        return bishop_moves + rook_moves
        
    def get_king_moves(self, position: BoardPosition, shallow=False) -> List[BoardPosition]:
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
        # Castling
        if shallow:
            return king_moves
        # Kingside
        if king.has_not_moved:
            bishop = self.square_at('f', file)
            knight = self.square_at('g', file)
            rook = self.square_at('h', file)
            if not (bishop.piece or knight.piece or
                    not rook.piece.__class__ is Rook or
                    not rook.piece.has_not_moved or
                    self.square_attacked(bishop, color) or 
                    self.square_attacked(knight, color)):
                king_moves.append(knight)
            # Queenside
            queen = self.square_at('d', file)
            bishop = self.square_at('c', file)
            knight = self.square_at('b', file)
            rook = self.square_at('a', file)
            if not (queen.piece or bishop.piece or knight.piece or
                    not rook.piece.__class__ is Rook or
                    not rook.piece.has_not_moved or
                    self.square_attacked(queen, color) or
                    self.square_attacked(bishop, color)):
                king_moves.append(bishop)
        return king_moves

    def validate_moves(self, old_square: BoardPosition, potential_moves: List[BoardPosition]) -> List[BoardPosition]:
        """Ensure none of the potential moves leave the player's king in check."""
        valid_moves = []
        for new_square in potential_moves:
            moving_piece = old_square.piece
            target_piece = new_square.piece
            new_square.piece = moving_piece
            old_square.piece = None
            if not self.king_in_check(self.current_turn):
                valid_moves.append(new_square)
            new_square.piece = target_piece
            old_square.piece = moving_piece
        return valid_moves
    
    def king_in_check(self, color: PieceColor) -> bool:
        targeted_squares = []
        king_at = None
        for rank in self.all_ranks():
            for file in self.all_files():
                square = self.square_at(rank, file)
                if not square.piece:
                    continue
                if square.piece.color is color and square.piece.__class__ is King:
                    king_at = square
                if square.piece.color is color:
                    continue
                targeted_squares += self.get_legal_moves(square, shallow=True)
        return king_at in targeted_squares
    
    def square_attacked(self, square: BoardPosition, defend_color: PieceColor) -> bool:
        for rank in self.all_ranks():
            for file in self.all_files():
                attacking_square = self.square_at(rank, file)
                if not attacking_square.piece:
                    continue
                if attacking_square.piece.color is defend_color:
                    continue
                if square in self.get_legal_moves(attacking_square, shallow=True):
                    return True
        return False

    def game_status(self) -> GameStatus:
        for rank in self.all_ranks():
            for file in self.all_files():
                square = self.square_at(rank, file)
                if not square.piece:
                    continue
                if square.piece.color is not self.current_turn:
                    continue
                if self.get_legal_moves(square):
                    return GameStatus.PLAY
        in_check = self.king_in_check(self.current_turn)
        if in_check:
            print(f"Checkmate! {self.current_turn} lost.")
            return GameStatus.CHECKMATE
        print("Stalemate!")
        return GameStatus.STALEMATE
        
    def reset_board(self) -> None:
        for rank in self.all_ranks():
            for file in self.all_files():
                self.square_at(rank, file).piece = None
        # Pawns
        for rank in self.all_ranks():
            self.square_at(rank, 2).piece = Pawn(PieceColor.WHITE)
            self.square_at(rank, 7).piece = Pawn(PieceColor.BLACK)
        # Rooks
        self.square_at('a', 1).piece = Rook(PieceColor.WHITE)
        self.square_at('h', 1).piece = Rook(PieceColor.WHITE)
        self.square_at('a', 8).piece = Rook(PieceColor.BLACK)
        self.square_at('h', 8).piece = Rook(PieceColor.BLACK)
        # Knights
        self.square_at('b', 1).piece = Knight(PieceColor.WHITE)
        self.square_at('g', 1).piece = Knight(PieceColor.WHITE)
        self.square_at('b', 8).piece = Knight(PieceColor.BLACK)
        self.square_at('g', 8).piece = Knight(PieceColor.BLACK)
        # Bishops
        self.square_at('c', 1).piece = Bishop(PieceColor.WHITE)
        self.square_at('f', 1).piece = Bishop(PieceColor.WHITE)
        self.square_at('c', 8).piece = Bishop(PieceColor.BLACK)
        self.square_at('f', 8).piece = Bishop(PieceColor.BLACK)
        # Queens
        self.square_at('d', 1).piece = Queen(PieceColor.WHITE)
        self.square_at('d', 8).piece = Queen(PieceColor.BLACK)
        # Kings
        self.square_at('e', 1).piece = King(PieceColor.WHITE)
        self.square_at('e', 8).piece = King(PieceColor.BLACK)

