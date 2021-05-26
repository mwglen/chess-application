from piece import Piece, PieceType, Color
from enum import Enum, auto

class InvalidMove(Exception):
    errors = {
        1: "Move must be valid SAN",
        2: "Could not find piece to move",
        3: "Specify column of piece to move",
        4: "{sf} does not have a piece on it",
        5: "The piece on {sf} cannot go to {st}",
        6: "Cannot capture pieces of same color",
        7: "Cannot move under check",
        8: "Cannot castle while in check",
        9: "Cannot castle after moving rook",
        10: "Cannot castle after moving queen",
        11: "Cannot castle through pieces",
        12: "Cannnot castle through check",
    }
    def __init__(self, code: int):
        msg = InvalidMove.errors[code]
        super().__init__(msg)

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
        self.pop(sf, None)
   
    # Moves a piece in the position with validation.
    # Raises an InvalidMove exception if the move is
    # invalid
    def move_san(self, move: str, c: Color):
        cols = "abcdefgh"
        rows = "12345678"
        pieces = "NBRQK"

        if move == "O-O": self._castle(True, c)
        elif move == "O-O-O": self._castle(False, c)

        # Moves like: e4
        elif (
            len(move) == 2
            and move[0] in cols 
            and move[1] in rows
        ): self._move(c, move[-2:])
        
        # Moves like: exd5
        elif (
            len(move) == 4
            and move[0] in cols
            and move[1] == "x"
            and move[2] in cols
            and move[3] in rows
        ): self._move(c, move[-2:], "P", move[0])

        # Moves like: Nf3
        elif (
            len(move) == 3
            and move[0] in pieces
            and move[1] in cols
            and move[2] in rows
        ): self._move(c, move[-2:], move[0])

        # Moves Like: Nxf3
        elif (
            len(move) == 4
            and move[0] in pieces
            and move[1] == "x"
            and move[2] in cols
            and move[3] in rows
        ): self._move(c, move[-2:], move[0])

        # Moves Like: Ndf3
        elif (
            len(move) == 4
            and move[0] in pieces
            and move[1] in cols
            and move[2] in cols
            and move[3] in rows
        ): self._move(c, move[-2:], move[0], move[1])

        # Moves Like: Ndxf3
        elif (
            len(move) == 5
            and move[0] in pieces
            and move[1] in cols
            and move[2] in "x"
            and move[3] in cols
            and move[4] in rows
        ): self.find_sf(c, move[-2:], move[0], move[1])

        else: raise InvalidMove(1)
    
    def _move(self, c: Color, st: str, pt = "P", col: str = None):
        # Find the square that which piece is moving from
        sf = list(filter(lambda s: (
                self.get(s) 
                and self.get(s).type.as_letter() == pt
                and self.get(s).color == c
                and (not col or s[0] == col)
                and (self._sees(s, st) or self._can_take(s, st))
                ), self
            )
        )

        if len(sf) == 0: raise InvalidMove(2)
        elif len(sf) > 1: raise InvalidMove(3)
        else: sf = sf[0]

        # Get the pieces associated with the squares
        (fp, tp) = map(lambda s: self.get(s), [sf, st])

        # Convert strings to arrays of ascii characters
        (af, at) = map(lambda s: list(ord(i) for i in s), [sf, st])
        
        is_white = fp.color == Color.WHITE
        
        # Get the info of the player whose move it is
        info = self.white if is_white else self.black
        
        if not fp: raise InvalidMove(4)
        if not self._sees(sf, st) and not self._can_take(sf, st):
            raise InvalidMove(5)
        if tp and fp and tp.color == fp.color: raise InvalidMove(6)
        if info.in_check: raise InvalidMove(7)
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

        if info.in_check: raise InvalidMove(8)
        if info.rook_moved: raise InvalidMove(9)
        if info.king_moved: raise InvalidMove(10)
        
        # Check if castling is blocked by pieces
        cols_to_check = "fg" if short else "bcd"
        for col in cols_to_check:
            if self.get(col + row): raise InvalidMove(11)
            for square in self:
                if (
                    self[square].color != c 
                    and self._can_take(square, col + row)
                ): raise InvalidMove(12)

        # Move the rook and king
        if short:
            self.raw_move("h" + row, "f" + row)
            self.raw_move("e" + row, "g" + row)
        else:
            self.raw_move("a" + row, "d" + row)
            self.raw_move("e" + row, "c" + row)

    # Checks if a piece can take a pience on a certain square
    def _can_take(self, sf: str, st: str) -> bool:
        (fp, tp) = map(lambda s: self.get(s), [sf, st])
        (af, at) = map(lambda s: list(ord(i) for i in s), [sf, st])
        
        # In order for a piece on a square to take another piece
        # Both squares must have pieces on them and the squares
        # must be different
        if not (fp and tp and sf != st): return False

        # Pawns capture differently than they move
        if fp.type == PieceType.PAWN:
            offset = 1 if fp.color == Color.WHITE else -1
            return (
                abs(at[0] - af[0]) == 1 
                and af[1] + offset == at[1]
            )
        else: return self._sees(sf, st)

    # Checks if a piece on one square sees a different square
    def _sees(self, sf: str, st: str) -> bool:
        (fp, tp) = map(lambda s: self.get(s), [sf, st])
        (af, at) = map(lambda s: list(ord(i) for i in s), [sf, st])

        if fp.type in [PieceType.BISHOP, PieceType.QUEEN]:
            # Check if on diagonal
            if abs(af[0] - at[0]) == abs(af[1] - at[1]):
                # Get a list of the square between sf and st
                to_check = list(map(
                    lambda x: chr(x[0]) + chr(x[1]),
                    zip(range(af[0], at[0]), range(af[1], at[1]))
                ))[1:]
                
                # Check if there are no pieces between the squares
                if all(not self.get(i) for i in to_check): 
                    return True
        
        if fp.type in [PieceType.ROOK, PieceType.QUEEN]: 
            # Check if on same row or column (exclusive)
            if (
                (af[0] == at[0]) != (af[1] == at[1])
                and not self._pieces_between(sf, st)
            ): return True

        if fp.type == PieceType.KNIGHT:
            if ([abs(at[0] - af[0]), abs(at[1] - af[1])] 
                in [[1, 2], [2, 1]]): return True
        
        if fp.type == PieceType.KING:
            if abs(af[1] - at[1]) <= 1 and abs(af[0] - at[0]) <= 1:
                return True
        
        if fp.type == PieceType.PAWN:
            orig_row = 2 if fp.color == Color.WHITE else 7
            offset = 1 if fp.color == Color.WHITE else -1
            if (at[0] == af[0]):
                if at[1] == (af[1] + offset) and not self.get(st):
                    return True
                else: return (
                    int(sf[1]) == orig_row
                    and at[1] == (af[1] + 2*offset)
                    and not self.get(st)
                )
        return False
    
    # Checks if there are pieces between two squares
    # The two squres must be either on the same diagonal 
    # or the same column/row
    def _pieces_between(self, sf: str, st: str) -> bool:
        (af, at) = map(lambda s: list(ord(i) for i in s), [sf, st])

        # Get a list of the square between sf and st
        to_check = list(map(
            lambda x: chr(x[0]) + chr(x[1]),
            zip(range(af[0], at[0]), range(af[1], at[1]))
        ))[1:]

        # Check if there are no pieces between the squares
        if any(self.get(i) for i in to_check): return True
        else: return False



class PositionInfo:
    def __init__(self):
        self.king_moved = False
        self.short_moved = False
        self.long_moved = False
        self.in_check = False

