from enum import Enum, auto

# Types of pieces
class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    # Returns the letter corresponding to the piece type
    def as_letter(self) -> str:
        if self.name == "PAWN":
            return 'P'
        elif self.name == "KNIGHT":
            return 'N'
        elif self.name == "BISHOP":
            return 'B'
        elif self.name == "ROOK":
            return 'R'
        elif self.name == "QUEEN":
            return 'Q'
        elif self.name == "KING":
            return 'K'

# Possible colors for a piece
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# A piece with a specified color
class Piece:
    def __init__(self, pt: PieceType, c: Color):
        self.type = pt
        self.color = c

