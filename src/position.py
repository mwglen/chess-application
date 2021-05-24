from piece import Piece, PieceType, Color
from enum import Enum, auto

class InvalidMove(Exception):
    pass

# A class representing a chess board
class Position(dict):
    def base() -> "Position":
        # Create a dictionary to map positions to pieces
        board = {}

        # The layout of the pieces on the first and eigth row
        layout = [
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]

        # Position the pieces on the board
        for (col, pt) in zip("abcdefgh", layout):
            # Position the pawns
            for (row, c) in zip("27", Color):
                board[col + row] = Piece(PieceType.PAWN, c)
            # Position the other pieces
            for (row, c) in zip("18", Color):
                board[col + row] = Piece(pt, c)

        # Return the dictionary
        b = Position(board)
        b.white = PositionInfo()
        b.black = PositionInfo()
        return b
    
    # Moves a piece in the position. This does not check to see
    # if the move is valid. It also overrites whatever is in
    # square_to (the square the piece is being moved to) and
    # erasing the piece in square_from (the square the piece is
    # being moved from)
    def raw_move(self, sf: str, st: str):
        self[st] = self[sf]
        self[sf] = {}
   
    # Moves a piece in the position with validation.
    # Raises an InvalidMove exception if the move is
    # invalid
    def move(self, move: str, c: Color):
        if move == "O-O": self._castle(True, c)
        elif move == "O-O-O": self._castle(False, c)
        else:
            pass
    
    def move(self, sf: str, st: str):
        fp = self.get(sf)
        tp = self.get(st)
        f_col = ord(sf[0])
        f_row = ord(sf[1])
        t_col = ord(st[0])
        t_row = ord(st[1])
        is_white = fp.color == Color.WHITE
        
        # Get the info of the player whose move it is
        info = self.white if is_white else self.black
        
        if fp == None:
            raise InvalidMove("{sf} does not have a piece on it")

        if not self._sees(sf, st) and not self._can_take(sf, st):
            raise InvalidMove(f"The piece on {sf} cannot go to {st}")

        if tp != None and fp != None and tp.color == fp.color:
            raise InvalidMove("Cannot capture pieces of same color")

        if info.in_check:
            raise InvalidMove("Cannot move under check")

        self.raw_move(sf, st)
        
        # Update Info
        if fp.type == PieceType.KING: info.king_moved = True
        elif fp.type == PieceType.ROOK and sf[1] == "a":
            info.long_moved = True
        elif fp.type == PieceType.ROOK and sf[1] == "h":
            info.short_moved = True

    def _castle(self, short: bool, c: Color):
        # Get the info of the player whose move it is
        info = self.white if c == Color.WHITE else self.black

        # Check if the rook has been moved
        rook_moved = info.short_moved if short else info.long_moved

        # Get the row on which the king and rook lie
        row = "1" if c == Color.WHITE else "8"

        if info.in_check: 
            raise InvalidMove("Cannot castle while in check")
        if info.rook_moved:
            raise InvalidMove("Cannot castle after moving rook")
        if info.king_moved:
            raise InvalidMove("Cannot castle after moving queen")
        
        # Check if castling is blocked by pieces
        cols_to_check = "fg" if short else "bcd"
        for col in cols_to_check:
            if self[col + row] != None: 
                raise InvalidMove("Cannot castle through pieces")
            for square in self:
                if self[square].color != c and self._can_take(square, col + row):
                    raise InvalidMove("Cannnot castle through check")

        # Move the rook and king
        if short:
            self.raw_move("h" + row, "f" + row)
            self.raw_move("e" + row, "g" + row)
        else:
            self.raw_move("a" + row, "d" + row)
            self.raw_move("e" + row, "c" + row)

    # Checks if a piece on one square sees a different square
    def _sees(self, sf: str, st: str) -> bool:
        fp = self.get(sf)
        tp = self.get(st)
        f_col = ord(sf[0])
        f_row = ord(sf[1])
        t_col = ord(st[0])
        t_row = ord(st[1])

        # Pawns capture differently than they move
        if fp.type == PieceType.PAWN:
            orig_row = 2 if fp.color == Color.WHITE else 7
            offset = 1 if fp.color == Color.WHITE else -1
            if int(sf[1]) == orig_row: offset *= 2
            return t_col == f_col and t_row == (f_row + offset)
        else:
            return self._can_take(sf, st)


    # Checks if a piece can take a pience on a certain square
    def _can_take(self, sf: str, st: str) -> bool:
        fp = self.get(sf)
        tp = self.get(st)
        f_col = ord(sf[0])
        f_row = ord(sf[1])
        t_col = ord(st[0])
        t_row = ord(st[1])

        # If there is no piece on from_square, 
        # then it can't see to_square
        if fp == None: return False

        # Squares see themself, as long as there is a piece on it
        if sf == st: return True

        if fp.type in [PieceType.BISHOP, PieceType.QUEEN]:
            # Check if on diagonal
            if abs(f_col - t_col) == abs(f_row - t_row):
                # Get a list of the columns and rows between the squares
                cols = range(f_col, t_col)
                rows = range(f_row, t_row)

                # Check if there is any pieces between the squares
                for col, row in zip(cols, rows):
                    # Ignore the first iteration
                    if col == f_col: continue
                    
                    # Check whether or the current square is empty
                    empty = self[chr(col) + chr(row)] == None
                    
                    # If we find that the last square is empty, return true
                    if empty and (col == range(f_col, t_col)[-1]): return True

                    # If we find that a square is not empty
                    # then the path must be blocked
                    if not empty: break

        
        if fp.type in [PieceType.ROOK, PieceType.QUEEN]: 
            # Check if on same row or column (exclusive)
            if f_col == t_col ^ f_row == t_row:
                # Get a list of the columns and rows between the squares
                cols = range(f_col, t_col)
                rows = range(f_row, t_row)

                # Check if there are any pieces between them
                for col in cols:
                    for row in rows:
                        # Ignore the first iteration
                        if col == f_col and row == f_row: continue
                        
                        # Check whether or the current square is empty
                        empty = self[chr(col) + chr(row)] == None
                        
                        # If we find that the last square is empty, return true
                        last_col = col == range(f_col, t_col)[-1]
                        last_row = row == range(f_row, t_row)[-1]
                        if empty and last_col and last_row: return True

                        # If we find that a square is not empty
                        # then the path must be blocked
                        if not empty: break

        
        if fp.type == PieceType.KNIGHT:
            if [abs(t_col - f_col), abs(t_row - f_row)] in [[1, 2], [2, 1]]:
                return True
        
        if fp.type == PieceType.KING:
            if abs(f_row - t_row) <= 1 and abs(f_col - t_col) <= 1:
                return True
        
        if fp.type == PieceType.PAWN:
            offset = 1 if fp.color == Color.WHITE else -1
            if abs(t_col - f_col) == 1 and t_row == f_row + offset: 
                return True

        return False

class PositionInfo:
    def __init__(self):
        self.king_moved = False
        self.short_moved = False
        self.long_moved = False
        self.in_check = False

