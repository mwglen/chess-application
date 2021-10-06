from enum import Enum, auto

# Types of pieces
class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    # Returns the letter corresponding to the piece type
    def as_letter(self) -> str:
        letters = ['P', 'N', 'B', 'R', 'Q', 'K']
        return letters[self.value]

    def as_unicode(self) -> str:
        return chr(0x2659 - self.value)
    
    def as_ascii(self) -> str:
        return "()\n)(\n/__\\"

# Possible colors for a piece
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# A piece with a specified color
class Piece:
    def __init__(self, pt: PieceType, c: Color):
        self.type = pt
        self.color = c

    def as_unicode(self) -> str:
        char = '\u2659' if self.color == Color.WHITE else '\u265F'
        return char - self.type
