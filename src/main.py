import curses
from enum import Enum, auto

def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()

    # Do something
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    stdscr.bkgd(" ", curses.color_pair(2))
    stdscr.box("|", "-")
    stdscr.addstr(0, 0, "Chess Application", curses.color_pair(1))
    
    board = Board.with_base_pos()

    stdscr.getch()

# A class representing a chess board
class Board(dict):
    def with_base_pos() -> dict:
        # Create a dictionary to map positions to pieces
        board = {}

        # The layout of the pieces on the first and eigth row
        layout = [
            PieceType.PAWN,
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
                board[col + row] = Piece(c, PieceType.PAWN)
            # Position the other pieces
            for (row, c) in zip("18", Color):
                board[col + row] = Piece(c, pt)

        # Return the dictionary
        return board

# Types of pieces
class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

# Possible colors for a piece
class Color(Enum):
    WHITE = auto()
    BLACK = auto()

# A piece with a specified color
class Piece:
    def __init__(self, pt: PieceType, c: Color):
        self.type = pt
        self.color = c

curses.wrapper(main)
